// Judges the Lua a mod ships against the engine's own sandbox policy
// (src/mods/Sandbox.lua: DENIED, DENIED_PREFIX, NETWORK).
//
// Archives are parsed in memory: nothing is written to disk and nothing is
// executed, so a hostile zip gets no filesystem to escape into.

import { inflateRawSync } from 'node:zlib';

export const DENIED = {
  io: 'the filesystem',
  os: 'the filesystem',
  debug: 'the debug library',
  package: 'the module loader',
  ffi: 'arbitrary C calls',
};
export const DENIED_PREFIX = ['love', 'ffi', 'jit'];
export const NETWORK = ['socket', 'enet', 'http', 'https', 'ssl', 'mime', 'ltn12'];

// Paths the mod sandbox never governs: a love.thread worker runs in its own
// Lua state, and a test file runs on the author's machine. Findings there are
// reported, not blocking.
export const NON_RUNTIME = [
  /(^|\/)tests?\//i,
  /(^|\/)spec\//i,
  /_test\.lua$/i,
  /_spec\.lua$/i,
  /(^|\/)workers?\//i,
  /_worker\.lua$/i,
];

export function isRuntimePath(name) {
  return !NON_RUNTIME.some((re) => re.test(name));
}

const SUSPECT = [
  [/\bloadstring\s*\(/g, 'loadstring() builds a chunk at runtime, which a scan cannot read'],
  [/(?<![.:\w])load\s*\(/g, 'load() builds a chunk at runtime, which a scan cannot read'],
  [/\bdofile\s*\(/g, 'dofile() runs a file off the real filesystem'],
  [/\bloadfile\s*\(/g, 'loadfile() reads a chunk off the real filesystem'],
  [/\bstring\s*\.\s*dump\s*\(/g, 'string.dump() reads function bytecode'],
  [/\bgetfenv\s*\(/g, 'getfenv() reaches for another function environment'],
  [/\bsetfenv\s*\(/g, 'setfenv() replaces a function environment'],
  [/\bjit\s*\.\s*util\b/g, 'jit.util exposes bytecode and constants'],
  [/\brawset\s*\(\s*_G\b/g, 'rawset on _G writes past the sandbox table'],
  [/\b_G\s*\[/g, '_G is indexed by a computed key'],
  [/\bdebug\s*\.\s*(getupvalue|setupvalue|getinfo|getlocal|sethook|getregistry)\b/g,
    'the debug library reads or rewrites live state'],
];

export function lineOf(src, index) {
  return src.slice(0, index).split('\n').length;
}

// Blanks what is not code the chunk itself runs: comments, and long-bracket
// strings, which is how a mod carries love.thread worker source. Short quoted
// strings stay, because that is where a require names its target.
export function stripComments(src) {
  let out = '';
  let i = 0;
  const blank = (stop) => {
    out += src.slice(i, stop).replace(/[^\n]/g, ' ');
    i = stop;
  };
  while (i < src.length) {
    if (src[i] === '-' && src[i + 1] === '-') {
      const long = /^--\[(=*)\[/.exec(src.slice(i, i + 16));
      if (long) {
        const end = src.indexOf(`]${long[1]}]`, i);
        blank(end === -1 ? src.length : end + long[1].length + 2);
        continue;
      }
      const nl = src.indexOf('\n', i);
      blank(nl === -1 ? src.length : nl);
      continue;
    }
    if (src[i] === '[') {
      const long = /^\[(=*)\[/.exec(src.slice(i, i + 16));
      if (long) {
        const end = src.indexOf(`]${long[1]}]`, i);
        blank(end === -1 ? src.length : end + long[1].length + 2);
        continue;
      }
    }
    out += src[i];
    i += 1;
  }
  return out;
}

export function scanSource(src, permissions = []) {
  const errors = [];
  const warnings = [];
  const re = /\brequire\s*(?:\(\s*)?([^)\n;]{0,120})/g;
  let m;
  while ((m = re.exec(src))) {
    const arg = m[1].trim();
    const line = lineOf(src, m.index);
    const literal = /^(['"])(.*?)\1/.exec(arg);
    if (!literal) {
      if (arg) warnings.push({ line, message: `require(${trunc(arg)}) is built at runtime, so its target cannot be read here` });
      continue;
    }
    const name = literal[2];
    const root = name.split('.')[0];
    if (DENIED[root]) {
      errors.push({ line, message: `require("${name}") — the sandbox denies ${root} (it grants ${DENIED[root]})` });
    } else if (DENIED_PREFIX.includes(root) && name !== root) {
      errors.push({ line, message: `require("${name}") — the sandbox denies ${root}.* submodules` });
    } else if (NETWORK.includes(root) && !permissions.includes('network')) {
      errors.push({ line, message: `require("${name}") needs "network" in the entry's permissions` });
    }
  }
  for (const [pattern, why] of SUSPECT) {
    pattern.lastIndex = 0;
    let hit;
    while ((hit = pattern.exec(src))) warnings.push({ line: lineOf(src, hit.index), message: why });
  }
  return { errors, warnings };
}

export function scanFiles(files, permissions = []) {
  const errors = [];
  const warnings = [];
  for (const { name, text } of files) {
    const found = scanSource(stripComments(text), permissions);
    const runtime = isRuntimePath(name);
    for (const e of found.errors) {
      if (runtime) errors.push({ name, ...e });
      else warnings.push({ name, ...e, message: `${e.message} (outside the sandbox: not mod runtime code)` });
    }
    for (const w of found.warnings) warnings.push({ name, ...w });
  }
  return { errors, warnings, files: files.length };
}

// One repo can publish several mods, so the first .zip in a release is not
// necessarily this entry's. Same order as build-index.mjs and ModUpdate.lua:
// <id>-<version>.zip, then a zip named for the id, then whatever is there.
export function pickZipAsset(assets, modId, version) {
  if (!Array.isArray(assets)) return null;
  const prefer = modId && version ? `${modId}-${version}.zip`.toLowerCase() : null;
  let idPrefixZip = null;
  let anyZip = null;
  for (const asset of assets) {
    const name = asset?.name;
    if (typeof name !== 'string' || !name.toLowerCase().endsWith('.zip')) continue;
    if (prefer && name.toLowerCase() === prefer) return asset.browser_download_url;
    if (modId && !idPrefixZip && name.toLowerCase().startsWith(modId.toLowerCase())) {
      idPrefixZip = asset.browser_download_url;
    }
    if (!anyZip) anyZip = asset.browser_download_url;
  }
  return idPrefixZip || anyZip;
}

export async function resolveZip(meta, token = '') {
  if (meta.downloadURL) return meta.downloadURL;
  if (!meta.github) return null;
  const res = await fetch(`https://api.github.com/repos/${meta.github}/releases?per_page=10`, {
    headers: {
      Accept: 'application/vnd.github+json',
      'User-Agent': 'gen1recomp-mod-index',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
  });
  if (!res.ok) throw new Error(`GitHub ${res.status} listing releases for ${meta.github}`);
  for (const release of await res.json()) {
    const version = /^\d+\.\d+\.\d+/.exec(String(release.tag_name ?? '').replace(/^[vV]/, ''))?.[0];
    const url = pickZipAsset(release.assets, meta.id, version);
    if (url) return url;
  }
  return null;
}

export async function luaFilesIn(url, limits = {}) {
  const maxZip = limits.maxZip ?? 64 * 1024 * 1024;
  const res = await fetch(url, { redirect: 'follow', signal: AbortSignal.timeout(60000) });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  const buf = Buffer.from(await res.arrayBuffer());
  if (buf.byteLength > maxZip) throw new Error(`zip is ${buf.byteLength} bytes, over the cap`);
  return readZipLua(buf, limits.maxUnpacked ?? 256 * 1024 * 1024);
}

// Every entry in the archive, from the central directory alone: no
// decompression, and CRC32 comes free for comparing bytes against a known copy.
export function listZip(buf) {
  const eocd = findEOCD(buf);
  if (eocd < 0) throw new Error('no end-of-central-directory record');
  const total = buf.readUInt16LE(eocd + 10);
  let offset = buf.readUInt32LE(eocd + 16);
  if (total === 0xffff || offset === 0xffffffff) throw new Error('zip64 is not supported here');
  const out = [];
  for (let i = 0; i < total; i += 1) {
    if (buf.readUInt32LE(offset) !== 0x02014b50) throw new Error('central directory is malformed');
    const crc = buf.readUInt32LE(offset + 16);
    const size = buf.readUInt32LE(offset + 24);
    const nameLen = buf.readUInt16LE(offset + 28);
    const extraLen = buf.readUInt16LE(offset + 30);
    const commentLen = buf.readUInt16LE(offset + 32);
    const name = buf.toString('utf8', offset + 46, offset + 46 + nameLen);
    offset += 46 + nameLen + extraLen + commentLen;
    if (!name.endsWith('/')) out.push({ name, size, crc: crc >>> 0 });
  }
  return out;
}

export async function zipBuffer(url, maxZip = 512 * 1024 * 1024) {
  const res = await fetch(url, { redirect: 'follow', signal: AbortSignal.timeout(120000) });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  const buf = Buffer.from(await res.arrayBuffer());
  if (buf.byteLength > maxZip) throw new Error(`zip is ${buf.byteLength} bytes, over the cap`);
  return buf;
}

export function readZipLua(buf, maxUnpacked = 256 * 1024 * 1024) {
  const eocd = findEOCD(buf);
  if (eocd < 0) throw new Error('no end-of-central-directory record');
  const total = buf.readUInt16LE(eocd + 10);
  let offset = buf.readUInt32LE(eocd + 16);
  if (total === 0xffff || offset === 0xffffffff) throw new Error('zip64 is not supported here');

  const out = [];
  let unpacked = 0;
  for (let i = 0; i < total; i += 1) {
    if (buf.readUInt32LE(offset) !== 0x02014b50) throw new Error('central directory is malformed');
    const method = buf.readUInt16LE(offset + 10);
    const compressed = buf.readUInt32LE(offset + 20);
    const size = buf.readUInt32LE(offset + 24);
    const nameLen = buf.readUInt16LE(offset + 28);
    const extraLen = buf.readUInt16LE(offset + 30);
    const commentLen = buf.readUInt16LE(offset + 32);
    const localAt = buf.readUInt32LE(offset + 42);
    const name = buf.toString('utf8', offset + 46, offset + 46 + nameLen);
    offset += 46 + nameLen + extraLen + commentLen;

    if (!name.toLowerCase().endsWith('.lua')) continue;
    unpacked += size;
    if (unpacked > maxUnpacked) throw new Error('unpacked size is over the cap');

    if (buf.readUInt32LE(localAt) !== 0x04034b50) throw new Error(`local header is malformed for ${name}`);
    const dataAt = localAt + 30 + buf.readUInt16LE(localAt + 26) + buf.readUInt16LE(localAt + 28);
    const raw = buf.subarray(dataAt, dataAt + compressed);
    if (method === 0) out.push({ name, text: raw.toString('utf8') });
    else if (method === 8) out.push({ name, text: inflateRawSync(raw, { maxOutputLength: maxUnpacked }).toString('utf8') });
  }
  return out;
}

function findEOCD(buf) {
  const min = Math.max(0, buf.byteLength - 66560);
  for (let i = buf.byteLength - 22; i >= min; i -= 1) {
    if (buf.readUInt32LE(i) === 0x06054b50) return i;
  }
  return -1;
}

function trunc(s) {
  return s.length > 40 ? `${s.slice(0, 40)}…` : s;
}
