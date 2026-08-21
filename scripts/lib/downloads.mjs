import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';

export const HISTORY_DAYS = 35;
export const RECENT_WINDOW_DAYS = 30;
const DAY_MS = 86400000;

export function downloadsStatePath(repoRoot) {
  return resolve(repoRoot, process.env.DOWNLOADS_STATE || '.health/downloads.json');
}

export function loadDownloads(path) {
  if (existsSync(path)) {
    try {
      const doc = JSON.parse(readFileSync(path, 'utf8'));
      if (doc?.version === 1 && doc.mods && typeof doc.mods === 'object') return doc;
    } catch {}
  }
  return { version: 1, mods: {} };
}

export function saveDownloads(path, state) {
  mkdirSync(dirname(path), { recursive: true });
  const mods = {};
  for (const folder of Object.keys(state.mods).sort()) mods[folder] = state.mods[folder];
  writeFileSync(path, `${JSON.stringify({ version: 1, mods }, null, 2)}\n`);
}

export function zipDownloadsByTag(releases) {
  const byTag = {};
  if (!Array.isArray(releases)) return byTag;
  for (const release of releases) {
    const tag = release?.tag_name;
    if (typeof tag !== 'string' || !Array.isArray(release.assets)) continue;
    let total = 0;
    let sawZip = false;
    for (const asset of release.assets) {
      if (typeof asset?.name !== 'string' || !asset.name.toLowerCase().endsWith('.zip')) continue;
      sawZip = true;
      total += Number.isFinite(asset.download_count) ? asset.download_count : 0;
    }
    if (sawZip) byTag[tag] = total;
  }
  return byTag;
}

export function record(state, folder, byTag, nowIso) {
  const entry = state.mods[folder] ?? { tags: {}, total: 0, as_of: nowIso, history: [] };
  for (const [tag, count] of Object.entries(byTag)) {
    entry.tags[tag] = Math.max(entry.tags[tag] ?? 0, count);
  }
  entry.total = Object.values(entry.tags).reduce((sum, n) => sum + n, 0);
  entry.as_of = nowIso;
  entry.history = trimHistory(
    [...(entry.history ?? []).filter((s) => dayOf(s.at) !== dayOf(nowIso)), { at: nowIso, total: entry.total }],
    nowIso,
  );
  state.mods[folder] = entry;
  return entry;
}

export function pruneDownloads(state, folders) {
  const keep = new Set(folders);
  for (const folder of Object.keys(state.mods)) {
    if (!keep.has(folder)) delete state.mods[folder];
  }
  return state;
}

export function summarize(entry, nowIso) {
  if (!entry || !Number.isFinite(entry.total)) return null;
  const now = Date.parse(nowIso);
  const history = trimHistory(entry.history ?? [], nowIso);
  const cutoff = now - RECENT_WINDOW_DAYS * DAY_MS;
  const aged = history.filter((s) => Date.parse(s.at) <= cutoff);
  const base = aged.length ? aged[aged.length - 1] : history.find((s) => s.at !== entry.as_of) ?? null;
  if (!base) return { total: entry.total, recent: null, window_days: null, as_of: entry.as_of };
  const days = Math.max(1, Math.round((now - Date.parse(base.at)) / DAY_MS));
  return {
    total: entry.total,
    recent: Math.max(0, entry.total - base.total),
    window_days: days,
    as_of: entry.as_of,
  };
}

function trimHistory(history, nowIso) {
  const floor = Date.parse(nowIso) - HISTORY_DAYS * DAY_MS;
  return history
    .filter((s) => Number.isFinite(Date.parse(s?.at)) && Date.parse(s.at) >= floor && Number.isFinite(s.total))
    .sort((a, b) => Date.parse(a.at) - Date.parse(b.at));
}

function dayOf(iso) {
  return String(iso).slice(0, 10);
}
