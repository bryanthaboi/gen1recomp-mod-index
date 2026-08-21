#!/usr/bin/env node
// Refuses to list an entry blocklist.json names, so a resubmission fails CI
// rather than waiting for someone to recognise the name.
//
//   node scripts/check-blocklist.mjs [mods/Author@id ...]   # default: all

import { existsSync, readFileSync } from 'node:fs';
import { basename, dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { listModFolders } from './lib/index-rules.mjs';

const repoRoot = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const modsDir = join(repoRoot, 'mods');
const listPath = join(repoRoot, 'blocklist.json');

if (!existsSync(listPath)) {
  console.log('no blocklist.json — nothing to check');
  process.exit(0);
}
const blocklist = JSON.parse(readFileSync(listPath, 'utf8'));
const authors = new Map(Object.entries(blocklist.authors || {}).map(([k, v]) => [slug(k), v]));
const repos = new Map(Object.entries(blocklist.repos || {}).map(([k, v]) => [k.toLowerCase(), v]));

const targets = process.argv.slice(2).filter((a) => !a.startsWith('--'));
const folders = targets.length
  ? targets.map((t) => basename(t.replace(/\/+$/, ''))).filter((f) => existsSync(join(modsDir, f)))
  : listModFolders(modsDir);

let blocked = 0;
for (const folder of folders) {
  const metaPath = join(modsDir, folder, 'meta.json');
  let meta = {};
  if (existsSync(metaPath)) {
    try {
      meta = JSON.parse(readFileSync(metaPath, 'utf8'));
    } catch {
      meta = {};
    }
  }

  const repoHit = meta.github && repos.get(meta.github.toLowerCase());
  if (repoHit) {
    fail(folder, `repo "${meta.github}" is blocklisted since ${repoHit.since}: ${repoHit.reason}`);
    continue;
  }
  for (const name of [folder.split('@')[0], meta.author, (meta.github || '').split('/')[0]]) {
    const hit = name && authors.get(slug(name));
    if (hit) {
      fail(folder, `author "${name}" is blocklisted since ${hit.since}: ${hit.reason}`);
      break;
    }
  }
}

console.log(blocked ? `\n${blocked} blocklisted entr${blocked === 1 ? 'y' : 'ies'}.` : `\nNo blocklisted entries (${folders.length} checked).`);
process.exit(blocked ? 1 : 0);

function fail(folder, message) {
  blocked += 1;
  console.log(`BLOCKED  ${folder}: ${message}`);
}

function slug(s) {
  return String(s).toLowerCase().replace(/[^a-z0-9]/g, '');
}
