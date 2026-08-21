#!/usr/bin/env node
// Last check before an automated commit touches site/data/index.json.
//
//   node scripts/commit-guard.mjs
//
// Restores the committed generated_at when a rebuild changed nothing else, so
// a job that runs four times a day does not produce four empty commits, and
// refuses the commit outright when the rebuilt index lost more entries than
// INDEX_MAX_SHRINK — a build that silently drops listings is a bug, not news.
//
// Download totals move on their own, so a bare comparison would call every
// run a change. A delta under INDEX_DOWNLOAD_NOISE (or 2%, capped at 25) is
// treated as no news, and .health/downloads.json is restored alongside the
// index so the accumulator does not push the commit through by itself.

import { execFileSync } from 'node:child_process';
import { readFileSync, writeFileSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const repoRoot = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const relPath = 'site/data/index.json';
const indexPath = join(repoRoot, relPath);
const downloadsPath = '.health/downloads.json';
const MAX_SHRINK = num(process.env.INDEX_MAX_SHRINK, 6);
const NOISE_FLOOR = num(process.env.INDEX_DOWNLOAD_NOISE, 5);
const NOISE_PCT = 0.02;
const NOISE_CAP = 25;

let committedText;
try {
  committedText = execFileSync('git', ['show', `HEAD:${relPath}`], {
    cwd: repoRoot,
    encoding: 'utf8',
    maxBuffer: 64 * 1024 * 1024,
  });
} catch {
  console.log(`${relPath} is not in HEAD — leaving the rebuild alone`);
  process.exit(0);
}

const rebuiltText = readFileSync(indexPath, 'utf8');
if (rebuiltText === committedText) {
  console.log(`${relPath} is unchanged`);
  process.exit(0);
}

const before = count(committedText);
const after = count(rebuiltText);
const lost = before - after;
if (lost > MAX_SHRINK) {
  console.log(`::error::${relPath} would drop from ${before} to ${after} entries (${lost} lost, ceiling ${MAX_SHRINK}). Refusing to commit.`);
  process.exit(1);
}

if (sansTimestamp(committedText) === sansTimestamp(settleDownloads(committedText, rebuiltText))) {
  writeFileSync(indexPath, committedText);
  restoreFromHead(downloadsPath);
  console.log(`${relPath} changed only its generated_at and download noise — restored the committed copy`);
} else {
  console.log(`${relPath}: ${before} -> ${after} entries, keeping the rebuild`);
}

function count(text) {
  try {
    return JSON.parse(text).mods?.length ?? 0;
  } catch {
    return 0;
  }
}

function sansTimestamp(text) {
  try {
    const { generated_at: _drop, ...rest } = JSON.parse(text);
    return JSON.stringify(rest);
  } catch {
    return text;
  }
}

function settleDownloads(before, after) {
  let committedDoc;
  let rebuiltDoc;
  try {
    committedDoc = JSON.parse(before);
    rebuiltDoc = JSON.parse(after);
  } catch {
    return after;
  }
  const previous = new Map((committedDoc.mods ?? []).map((mod) => [mod.folder, mod.downloads]));
  for (const mod of rebuiltDoc.mods ?? []) {
    const was = previous.get(mod.folder);
    if (!was || !mod.downloads) continue;
    if (isNoise(was.total, mod.downloads.total)) mod.downloads = was;
  }
  return `${JSON.stringify(rebuiltDoc, null, 2)}\n`;
}

function isNoise(before, after) {
  if (!Number.isFinite(before) || !Number.isFinite(after)) return false;
  const drift = Math.abs(after - before);
  return drift <= Math.min(NOISE_CAP, Math.max(NOISE_FLOOR, before * NOISE_PCT));
}

function restoreFromHead(path) {
  try {
    const head = execFileSync('git', ['show', `HEAD:${path}`], {
      cwd: repoRoot,
      encoding: 'utf8',
      maxBuffer: 64 * 1024 * 1024,
    });
    writeFileSync(join(repoRoot, path), head);
    console.log(`${path} — restored the committed copy`);
  } catch {}
}

function num(raw, fallback) {
  const n = Number.parseInt(raw ?? '', 10);
  return Number.isFinite(n) && n >= 0 ? n : fallback;
}
