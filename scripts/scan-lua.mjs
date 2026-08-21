#!/usr/bin/env node
// Reads the Lua an entry actually ships and judges it against the mod
// sandbox's policy (scripts/lib/lua-scan.mjs).
//
//   node scripts/scan-lua.mjs [mods/Author@id ...]   # default: all
//
// Exit 1 when a file reaches for something the sandbox denies outright.
// Everything else is reported for a human to read: dynamic require and load()
// have honest uses, and a scan cannot prove intent.

import { appendFileSync, existsSync, readFileSync } from 'node:fs';
import { basename, dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { listModFolders } from './lib/index-rules.mjs';
import { luaFilesIn, resolveZip, scanFiles } from './lib/lua-scan.mjs';

const repoRoot = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const modsDir = join(repoRoot, 'mods');
const token = process.env.GITHUB_TOKEN || '';

const targets = process.argv.slice(2).filter((a) => !a.startsWith('--'));
const folders = targets.length
  ? targets.map((t) => basename(t.replace(/\/+$/, ''))).filter((f) => existsSync(join(modsDir, f)))
  : listModFolders(modsDir);

const reports = [];
let failed = 0;

for (const folder of folders) {
  const metaPath = join(modsDir, folder, 'meta.json');
  if (!existsSync(metaPath)) continue;

  let meta;
  try {
    meta = JSON.parse(readFileSync(metaPath, 'utf8'));
  } catch (err) {
    console.log(`skip     ${folder}: meta.json is unreadable (${err.message})`);
    continue;
  }

  let files;
  try {
    const url = await resolveZip(meta, token);
    if (!url) {
      console.log(`skip     ${folder}: no downloadable zip yet`);
      continue;
    }
    files = await luaFilesIn(url);
  } catch (err) {
    console.log(`skip     ${folder}: ${err.message}`);
    continue;
  }

  const { errors, warnings } = scanFiles(files, meta.permissions || []);
  const label = `${folder} (${files.length} lua file${files.length === 1 ? '' : 's'})`;
  if (errors.length) {
    failed += 1;
    console.log(`FAIL     ${label}`);
  } else if (warnings.length) {
    console.log(`review   ${label} — ${warnings.length} thing(s) a human should read`);
  } else {
    console.log(`ok       ${label}`);
  }
  for (const e of errors) console.log(`  denied ${e.name}:${e.line}  ${e.message}`);
  for (const w of warnings) console.log(`  review ${w.name}:${w.line}  ${w.message}`);
  if (errors.length || warnings.length) reports.push({ folder, errors, warnings });
}

writeSummary();
console.log(failed ? `\n${failed} entr${failed === 1 ? 'y' : 'ies'} reach past the sandbox.` : '\nNothing reaches past the sandbox.');
process.exit(failed ? 1 : 0);

function writeSummary() {
  const out = process.env.GITHUB_STEP_SUMMARY;
  if (!out || !reports.length) return;
  const lines = ['### Lua scan', ''];
  for (const r of reports) {
    lines.push(`#### \`${r.folder}\``, '');
    for (const e of r.errors) lines.push(`- **denied** \`${e.name}:${e.line}\` — ${e.message}`);
    for (const w of r.warnings) lines.push(`- review \`${w.name}:${w.line}\` — ${w.message}`);
    lines.push('');
  }
  appendFileSync(out, `${lines.join('\n')}\n`);
}
