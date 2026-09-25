#!/usr/bin/env node
// Fold mods/ and carts/ into the single file the site (and anything else)
// reads: site/data/index.json, plus copies of each entry's description.md and
// thumbnail so the published Pages site is self-contained.
//
//   node scripts/build-index.mjs                # metadata only
//   node scripts/build-index.mjs --releases     # also re-read GitHub Releases
//   GITHUB_TOKEN=... node scripts/build-index.mjs --releases   # 5000 req/h
//
// --releases is what keeps the index honest without a PR per version bump:
// entries with "github" and automatic_version_check get their newest
// installable release recorded, picked the same way the launcher's
// ModUpdate.pickZipAsset does (prefer <id>-<version>.zip, then <id>*.zip,
// then any .zip) so the site and the game agree on what "latest" means.
//
// The same response carries each asset's download_count, so cumulative
// download totals cost no extra request. They accumulate in .health/, never
// in mods/ -- an entry folder is contributor-owned and MI103 refuses anything
// but the four allowed files.

import { copyFileSync, existsSync, mkdirSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { loadModeration, isQuarantined } from './lib/moderation.mjs';
import {
  checkCartFolder,
  checkModFolder,
  listEntryFolders,
  loadCartSchema,
  loadSchema,
} from './lib/index-rules.mjs';
import {
  downloadsStatePath,
  loadDownloads,
  pruneDownloads,
  record,
  saveDownloads,
  summarize,
  zipDownloadsByTag,
} from './lib/downloads.mjs';

const repoRoot = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const modsDir = join(repoRoot, 'mods');
const cartsDir = join(repoRoot, 'carts');
const outDir = join(repoRoot, 'site', 'data');
const withReleases = process.argv.includes('--releases');
const token = process.env.GITHUB_TOKEN || '';
const moderation = loadModeration(join(repoRoot, '.health', 'moderation.json'));

const schema = loadSchema(repoRoot);
const cartSchema = loadCartSchema(repoRoot);
const downloadsPath = downloadsStatePath(repoRoot);
const downloads = loadDownloads(downloadsPath);
const now = new Date().toISOString();

// The submission page validates against the same schema with the same checker
// CI uses. Copying beats a second implementation drifting out of step.
mkdirSync(outDir, { recursive: true });
copyFileSync(join(repoRoot, 'schema', 'mod.schema.json'), join(outDir, 'mod.schema.json'));
copyFileSync(join(repoRoot, 'schema', 'cart.schema.json'), join(outDir, 'cart.schema.json'));
copyFileSync(join(repoRoot, 'scripts', 'lib', 'jsonschema.mjs'), join(repoRoot, 'site', 'assets', 'jsonschema.js'));

const mods = collect(modsDir, 'mods', schema, checkModFolder);
const carts = collect(cartsDir, 'carts', cartSchema, checkCartFolder);
const everything = [...mods, ...carts];

const cartRows = new Set(carts);
if (withReleases) {
  for (const entry of everything) {
    const ext = cartRows.has(entry) ? '.g1rcart' : '.zip';
    if (entry.update_check !== 'pending') continue;
    try {
      const releases = await fetchReleases(entry.github);
      entry.latest = pickRelease(releases, entry, ext);
      entry.update_check = entry.latest ? 'ok' : 'no installable release';
      record(downloads, entry.downloads_key, zipDownloadsByTag(releases, ext), now);
    } catch (err) {
      entry.update_check = `error: ${err.message}`;
      console.error(`${entry.folder}: ${err.message}`);
    }
  }
  pruneDownloads(downloads, everything.map((entry) => entry.downloads_key));
  saveDownloads(downloadsPath, downloads);
}

for (const entry of everything) {
  entry.downloads = summarize(downloads.mods[entry.downloads_key], now);
  delete entry.downloads_key;
}

mods.sort((a, b) => a.title.localeCompare(b.title));
carts.sort((a, b) => a.title.localeCompare(b.title));

const index = {
  // Bump when the shape changes in a way a consumer has to notice.
  schema_version: 1,
  generated_at: now,
  count: mods.length,
  cart_count: carts.length,
  categories: schema.properties.categories.items.enum,
  base_games: cartSchema.properties.base.enum,
  mods,
  carts,
};

mkdirSync(outDir, { recursive: true });
writeFileSync(join(outDir, 'index.json'), `${JSON.stringify(index, null, 2)}\n`);
console.log(
  `wrote site/data/index.json — ${mods.length} mod(s), ${carts.length} cart(s)${withReleases ? ', releases refreshed' : ''}`,
);

// ---------------------------------------------------------------- helpers

function collect(dir, root, entrySchema, check) {
  rmSync(join(outDir, root), { recursive: true, force: true });
  mkdirSync(join(outDir, root), { recursive: true });

  const rows = [];
  for (const folder of listEntryFolders(dir)) {
    if (isQuarantined(moderation, root, folder)) {
      console.log(`quarantined ${root}/${folder}: excluded from published index`);
      continue;
    }
    const from = join(dir, folder);
    const { meta, errors } = check(from, folder, entrySchema);
    if (!meta || errors.length) {
      console.error(`skipping ${folder}: ${errors[0] ?? 'unreadable meta.json'}`);
      continue;
    }

    const destDir = join(outDir, root, folder);
    mkdirSync(destDir, { recursive: true });
    copyFileSync(join(from, 'description.md'), join(destDir, 'description.md'));

    let thumbnail = null;
    for (const name of ['thumbnail.png', 'thumbnail.jpg']) {
      if (existsSync(join(from, name))) {
        copyFileSync(join(from, name), join(destDir, name));
        thumbnail = `data/${root}/${folder}/${name}`;
        break;
      }
    }

    const description = readFileSync(join(from, 'description.md'), 'utf8');
    rows.push({
      folder,
      ...meta,
      thumbnail,
      description_url: `data/${root}/${folder}/description.md`,
      summary: meta.summary || firstLine(description),
      latest: null,
      update_check: meta.github && meta.automatic_version_check !== false ? 'pending' : 'off',
      downloads: null,
      downloads_key: root === 'mods' ? folder : `${root}/${folder}`,
    });
  }
  return rows;
}

function firstLine(markdown) {
  for (const raw of markdown.split('\n')) {
    const line = raw.trim();
    if (!line || line.startsWith('#') || line.startsWith('!') || line.startsWith('>')) continue;
    return line.replace(/[*_`[\]]/g, '').slice(0, 200);
  }
  return '';
}

async function ghJson(url) {
  const res = await fetch(url, {
    headers: {
      Accept: 'application/vnd.github+json',
      'User-Agent': 'gen1recomp-mod-index',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
  });
  if (res.status === 404) return null;
  if (res.status === 403 && res.headers.get('x-ratelimit-remaining') === '0') {
    throw new Error('GitHub rate limit reached (set GITHUB_TOKEN)');
  }
  if (!res.ok) throw new Error(`GitHub ${res.status} for ${url}`);
  return res.json();
}

// Mirrors src/mods/ModUpdate.lua: prefer <id>-<version>.zip, then a zip whose
// name starts with the id, then the first zip in the release.
// Mods ship a .zip; a cart ships the single .g1rcart cartkit packs.
function pickZipAsset(assets, modId, version, ext = '.zip') {
  if (!Array.isArray(assets)) return null;
  const prefer = modId && version ? `${modId}-${version}${ext}` : null;
  let idPrefixZip = null;
  let anyZip = null;
  for (const asset of assets) {
    const name = asset?.name;
    if (typeof name !== 'string' || !name.toLowerCase().endsWith(ext)) continue;
    const row = { name, url: asset.browser_download_url, size: asset.size };
    if (prefer && name === prefer) return row;
    if (modId && !idPrefixZip && name.toLowerCase().startsWith(modId.toLowerCase())) idPrefixZip = row;
    if (!anyZip) anyZip = row;
  }
  return idPrefixZip || anyZip;
}

function parseRelease(doc, modId, ext) {
  const version = String(doc.tag_name ?? '').replace(/^[vV]/, '');
  const triple = /^\d+\.\d+\.\d+/.exec(version)?.[0];
  if (!triple) return null; // the launcher refuses non-semver tags too
  const zip = pickZipAsset(doc.assets, modId, triple, ext);
  if (!zip) return null;
  return {
    version: triple,
    tag: doc.tag_name,
    name: doc.name || triple,
    prerelease: doc.prerelease === true,
    published_at: doc.published_at,
    zip,
  };
}

async function fetchReleases(repo) {
  const releases = await ghJson(`https://api.github.com/repos/${repo}/releases?per_page=30`);
  return Array.isArray(releases) ? releases : [];
}

function pickRelease(releases, mod, ext) {
  if (releases.length === 0) return null;

  if (mod.fixed_release_tag) {
    const pinned = releases.find((r) => r.tag_name === mod.fixed_release_tag);
    return pinned ? parseRelease(pinned, mod.id, ext) : null;
  }
  const parsed = releases.map((r) => parseRelease(r, mod.id, ext)).filter(Boolean);
  return parsed.find((r) => !r.prerelease) ?? parsed[0] ?? null;
}
