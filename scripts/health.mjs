#!/usr/bin/env node
// Scheduled counterpart to check-links.mjs: probes every entry's distribution
// points, keeps a strike count per entry in .health/state.json, and deletes
// entries that stay broken for HEALTH_STRIKES consecutive runs.
//
//   node scripts/health.mjs                            # report only
//   node scripts/health.mjs --record                   # persist strike counts
//   node scripts/health.mjs --record --prune           # ...and delete entries past the limit
//   node scripts/health.mjs --removed-list out.txt     # write folder<TAB>reason lines
//
// Any tripped ceiling skips the whole run: no strikes recorded, nothing
// removed, and skip_run=true so the caller does not commit either.
//
// Env: GITHUB_TOKEN, HEALTH_STRIKES=4, HEALTH_MAX_REMOVALS=5,
//      HEALTH_MAX_NEW_DEAD=10, HEALTH_MAX_NEW_DEAD_PCT=10,
//      HEALTH_MAX_UNKNOWN_PCT=25, HEALTH_CONCURRENCY=6

import { appendFileSync, existsSync, mkdirSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { listModFolders } from './lib/index-rules.mjs';

const repoRoot = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const modsDir = join(repoRoot, 'mods');
const stateDir = join(repoRoot, '.health');
const statePath = join(stateDir, 'state.json');

const token = process.env.GITHUB_TOKEN || '';
const STRIKES = num(process.env.HEALTH_STRIKES, 4);
const MAX_REMOVALS = num(process.env.HEALTH_MAX_REMOVALS, 5);
const MAX_NEW_DEAD = num(process.env.HEALTH_MAX_NEW_DEAD, 10);
const MAX_NEW_DEAD_PCT = num(process.env.HEALTH_MAX_NEW_DEAD_PCT, 10);
const MAX_UNKNOWN_PCT = num(process.env.HEALTH_MAX_UNKNOWN_PCT, 25);
const CONCURRENCY = num(process.env.HEALTH_CONCURRENCY, 6);

const argv = process.argv.slice(2);
const prune = argv.includes('--prune');
const record = prune || argv.includes('--record');
const removedListPath = flagValue('--removed-list');

const folders = listModFolders(modsDir);
const results = await mapPool(folders, CONCURRENCY, probeEntry);

const broken = results.filter((r) => r.state === 'dead');
const unknown = results.filter((r) => r.state === 'unknown');
const healthy = results.filter((r) => r.state === 'ok');

const state = loadState();
const knownFailing = new Set(Object.keys(state.failing));
const newlyDead = broken.filter((r) => !knownFailing.has(r.folder));

const pct = (n) => (results.length ? Math.round((n / results.length) * 100) : 0);
const unknownPct = pct(unknown.length);
const newDeadPct = pct(newlyDead.length);

const notes = [];
let skipRun = false;

if (unknownPct > MAX_UNKNOWN_PCT) {
  skipRun = true;
  notes.push(
    `${unknown.length} of ${results.length} entries (${unknownPct}%) came back inconclusive, over the ${MAX_UNKNOWN_PCT}% ceiling. ` +
      'That reads as a network or API problem on this side, not as dead mods.',
  );
}

if (newlyDead.length > MAX_NEW_DEAD || (newlyDead.length >= 3 && newDeadPct > MAX_NEW_DEAD_PCT)) {
  skipRun = true;
  notes.push(
    `${newlyDead.length} entries broke at once (${newDeadPct}% of the index), over the ${MAX_NEW_DEAD}-entry / ${MAX_NEW_DEAD_PCT}% ceiling. ` +
      'Healthy mods do not fail in a batch — this reads as a GitHub outage or a bad probe.',
  );
}

const next = { version: 1, failing: structuredClone(state.failing) };
for (const r of results) {
  if (r.state === 'ok') {
    delete next.failing[r.folder];
  } else if (r.state === 'dead') {
    const prev = next.failing[r.folder];
    next.failing[r.folder] = {
      strikes: (prev?.strikes ?? 0) + 1,
      since: prev?.since ?? new Date().toISOString(),
      reason: r.reason,
    };
  }
}
for (const folder of Object.keys(next.failing)) {
  if (!folders.includes(folder)) delete next.failing[folder];
}

const doomed = Object.entries(next.failing)
  .filter(([, entry]) => entry.strikes >= STRIKES)
  .sort(([a], [b]) => a.localeCompare(b));

if (doomed.length > MAX_REMOVALS) {
  skipRun = true;
  notes.push(
    `${doomed.length} entries are past ${STRIKES} strikes, over the ${MAX_REMOVALS}-per-run ceiling. ` +
      'Confirm they are really gone, then rerun or raise HEALTH_MAX_REMOVALS.',
  );
}

const removed = [];
if (!skipRun) {
  if (prune) {
    for (const [folder, entry] of doomed) {
      rmSync(join(modsDir, folder), { recursive: true, force: true });
      delete next.failing[folder];
      removed.push({ folder, ...entry });
    }
  }
  if (record) writeState(next);
}

const effective = skipRun ? state : next;

for (const r of results) {
  if (r.state === 'ok') continue;
  console.log(`${r.state === 'dead' ? 'broken  ' : 'unknown '} ${r.folder}: ${r.reason}`);
}
console.log(`\n${healthy.length} ok, ${broken.length} broken, ${unknown.length} inconclusive`);
if (skipRun) console.log('\nRUN SKIPPED — nothing recorded, nothing removed, nothing to commit.');
for (const note of notes) console.log(`! ${note}`);
for (const r of removed) console.log(`removed  ${r.folder}: ${r.reason}`);

if (removedListPath) {
  writeFileSync(removedListPath, removed.map((r) => `${r.folder}\t${r.reason}\t${r.since}\n`).join(''));
}

writeSummary();
emit('dead_count', String(broken.length));
emit('new_dead_count', String(newlyDead.length));
emit('unknown_count', String(unknown.length));
emit('removed_count', String(removed.length));
emit('skip_run', skipRun ? 'true' : 'false');
emit('needs_review', skipRun || removed.length ? 'true' : 'false');
for (const note of notes) console.log(`::warning::${note}`);

// ---------------------------------------------------------------- probing

async function probeEntry(folder) {
  const metaPath = join(modsDir, folder, 'meta.json');
  if (!existsSync(metaPath)) return { folder, state: 'unknown', reason: 'no meta.json' };

  let meta;
  try {
    meta = JSON.parse(readFileSync(metaPath, 'utf8'));
  } catch (err) {
    return { folder, state: 'unknown', reason: `meta.json is unreadable (${err.message})` };
  }

  const checks = [];
  if (meta.github) checks.push(await probeRepo(meta.github));
  if (meta.downloadURL) checks.push(await probeDownload(meta.downloadURL));
  if (!checks.length) return { folder, state: 'unknown', reason: 'no github and no downloadURL' };

  const dead = checks.find((c) => c.state === 'dead');
  if (dead) return { folder, state: 'dead', reason: dead.reason };
  const stalled = checks.find((c) => c.state === 'unknown');
  if (stalled) return { folder, state: 'unknown', reason: stalled.reason };
  return { folder, state: 'ok', reason: checks.map((c) => c.reason).join('; ') };
}

async function probeRepo(slug) {
  let res;
  try {
    res = await fetch(`https://api.github.com/repos/${slug}`, {
      headers: {
        Accept: 'application/vnd.github+json',
        'User-Agent': 'gen1recomp-mod-index',
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
      },
      signal: AbortSignal.timeout(20000),
    });
  } catch (err) {
    return { state: 'unknown', reason: `github "${slug}" was unreachable (${err.message})` };
  }
  if ((res.status === 403 || res.status === 429) && res.headers.get('x-ratelimit-remaining') === '0') {
    return { state: 'unknown', reason: 'GitHub rate limit' };
  }
  if (res.status === 404) {
    return { state: 'dead', reason: `github "${slug}" returned 404 — deleted, renamed away, or made private` };
  }
  if (res.status === 451) {
    return { state: 'dead', reason: `github "${slug}" returned 451 — taken down` };
  }
  if (!res.ok) return { state: 'unknown', reason: `github "${slug}" returned HTTP ${res.status}` };
  return { state: 'ok', reason: `github "${slug}" ok` };
}

async function probeDownload(url) {
  let res;
  try {
    res = await fetch(url, { method: 'HEAD', redirect: 'follow', signal: AbortSignal.timeout(30000) });
    if (res.status === 405 || res.status === 501) {
      res = await fetch(url, {
        method: 'GET',
        redirect: 'follow',
        headers: { Range: 'bytes=0-0' },
        signal: AbortSignal.timeout(30000),
      });
      await res.body?.cancel().catch(() => {});
    }
  } catch (err) {
    return { state: 'unknown', reason: `downloadURL was unreachable (${err.message})` };
  }
  if (res.status === 404 || res.status === 410) {
    return { state: 'dead', reason: `downloadURL returned HTTP ${res.status}` };
  }
  if (!res.ok) return { state: 'unknown', reason: `downloadURL returned HTTP ${res.status}` };
  const type = res.headers.get('content-type') || '';
  if (/text\/html/i.test(type)) {
    return { state: 'dead', reason: `downloadURL serves ${type} instead of a .zip` };
  }
  return { state: 'ok', reason: `downloadURL ${res.status} ${type || 'no content-type'}` };
}

// ------------------------------------------------------------------ state

function loadState() {
  if (!existsSync(statePath)) return { version: 1, failing: {} };
  try {
    const parsed = JSON.parse(readFileSync(statePath, 'utf8'));
    return { version: 1, failing: parsed.failing ?? {} };
  } catch {
    return { version: 1, failing: {} };
  }
}

function writeState(value) {
  const ordered = {};
  for (const key of Object.keys(value.failing).sort()) ordered[key] = value.failing[key];
  mkdirSync(stateDir, { recursive: true });
  writeFileSync(statePath, `${JSON.stringify({ version: 1, failing: ordered }, null, 2)}\n`);
}

// ----------------------------------------------------------------- output

function writeSummary() {
  const out = process.env.GITHUB_STEP_SUMMARY;
  if (!out) return;
  const lines = [
    `### Index health — ${results.length} entries`,
    '',
    `- ${healthy.length} ok`,
    `- ${broken.length} broken (${newlyDead.length} new this run)`,
    `- ${unknown.length} inconclusive`,
    '',
  ];

  if (skipRun) {
    lines.push('> [!CAUTION]', '> **Run skipped.** Nothing was recorded, removed, or committed.', '');
  }
  for (const note of notes) lines.push('> [!WARNING]', `> ${note}`, '');

  const failing = Object.entries(effective.failing).sort(([a], [b]) => a.localeCompare(b));
  if (failing.length) {
    lines.push('#### On the clock', '', '| entry | strikes | failing since | reason |', '|---|---|---|---|');
    for (const [folder, entry] of failing) {
      lines.push(`| \`${folder}\` | ${entry.strikes}/${STRIKES} | ${entry.since} | ${entry.reason} |`);
    }
    lines.push('');
  }

  if (doomed.length && !removed.length) {
    lines.push(`#### Past ${STRIKES} strikes, not removed (${doomed.length})`, '');
    for (const [folder] of doomed) lines.push(`- \`${folder}\``);
    lines.push('');
  }

  if (removed.length) {
    lines.push(`#### Removed (${removed.length})`, '');
    for (const r of removed) lines.push(`- \`${r.folder}\` — ${r.reason} (failing since ${r.since})`);
    lines.push('');
  }

  appendFileSync(out, `${lines.join('\n')}\n`);
}

function emit(key, value) {
  const out = process.env.GITHUB_OUTPUT;
  if (out) appendFileSync(out, `${key}=${value}\n`);
}

// ---------------------------------------------------------------- helpers

async function mapPool(items, limit, fn) {
  const out = new Array(items.length);
  let next = 0;
  const worker = async () => {
    for (let i = next++; i < items.length; i = next++) out[i] = await fn(items[i]);
  };
  await Promise.all(Array.from({ length: Math.min(limit, items.length) }, worker));
  return out;
}

function flagValue(name) {
  const i = argv.indexOf(name);
  return i >= 0 && argv[i + 1] && !argv[i + 1].startsWith('--') ? argv[i + 1] : null;
}

function num(raw, fallback) {
  const n = Number.parseInt(raw ?? '', 10);
  return Number.isFinite(n) && n >= 0 ? n : fallback;
}
