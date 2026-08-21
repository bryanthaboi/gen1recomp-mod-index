#!/usr/bin/env node
// node --test scripts/test.mjs  (or: npm test)
//
// Covers the rules a submission is judged by, plus the markdown renderer the
// site uses on untrusted description text.

import { test } from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, mkdirSync, writeFileSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

import { validate } from './lib/jsonschema.mjs';
import { checkCollisions, checkModFolder, loadSchema } from './lib/index-rules.mjs';
import { pruneDownloads, record, summarize, zipDownloadsByTag } from './lib/downloads.mjs';
import { renderMarkdown } from '../site/assets/markdown.js';

const repoRoot = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const schema = loadSchema(repoRoot);

const GOOD_META = {
  id: 'my_mod',
  title: 'My Mod',
  author: 'Ash',
  version: '1.0.0',
  categories: ['GAMEPLAY'],
  repo: 'https://github.com/ash/my_mod',
  github: 'ash/my_mod',
};

function scratch(files, folder = 'Ash@my_mod') {
  const root = mkdtempSync(join(tmpdir(), 'modindex-'));
  const dir = join(root, folder);
  mkdirSync(dir, { recursive: true });
  for (const [name, content] of Object.entries(files)) {
    writeFileSync(join(dir, name), content);
  }
  return { dir, folder, cleanup: () => rmSync(root, { recursive: true, force: true }) };
}

const withEntry = (files, folder) => {
  const s = scratch(
    { 'meta.json': JSON.stringify(GOOD_META), 'description.md': 'What it does.\n', ...files },
    folder,
  );
  try {
    return checkModFolder(s.dir, s.folder, schema);
  } finally {
    s.cleanup();
  }
};

const messages = (result) => [...result.errors, ...result.warnings].join('\n');

// ------------------------------------------------------------------- schema

test('a complete entry validates', () => {
  assert.deepEqual(validate(GOOD_META, schema), []);
});

test('required fields are required', () => {
  const { id, ...rest } = GOOD_META;
  assert.match(validate(rest, schema).join(), /missing required field "id"/);
});

test('unknown fields are refused, so a typo cannot go unnoticed', () => {
  assert.match(validate({ ...GOOD_META, downlodUrl: 'x' }, schema).join(), /unknown field "downlodUrl"/);
});

test('version has to be semver', () => {
  assert.match(validate({ ...GOOD_META, version: '1.0' }, schema).join(), /version.*does not match/);
});

test('categories come from the fixed vocabulary', () => {
  assert.match(validate({ ...GOOD_META, categories: ['STUFF'] }, schema).join(), /is not one of/);
});

test('github must be owner/repo, not a URL', () => {
  assert.match(validate({ ...GOOD_META, github: 'https://github.com/ash/my_mod' }, schema).join(), /github/);
});

// -------------------------------------------------------------------- layout

test('a well-formed folder passes clean', () => {
  const result = withEntry({});
  assert.deepEqual(result.errors, []);
});

test('the folder id half has to match meta.json', () => {
  assert.match(messages(withEntry({}, 'Ash@other_mod')), /MI202/);
});

test('the folder author half may be punctuation-stripped but not different', () => {
  assert.deepEqual(withEntry({ 'meta.json': JSON.stringify({ ...GOOD_META, author: 'A. Ketchum' }) }, 'AKetchum@my_mod').errors, []);
  assert.match(messages(withEntry({ 'meta.json': JSON.stringify(GOOD_META) }, 'Gary@my_mod')), /MI202/);
});

test('description.md is required and cannot be empty', () => {
  assert.match(messages(withEntry({ 'description.md': '' })), /MI104/);
});

test('stray files are refused — an index entry is metadata only', () => {
  assert.match(messages(withEntry({ 'main.lua': 'print("hi")' })), /MI103/);
});

test('a thumbnail has to be the image it claims to be', () => {
  assert.match(messages(withEntry({ 'thumbnail.png': 'not a png' })), /MI106/);
  assert.deepEqual(withEntry({ 'thumbnail.png': Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d]) }).errors, []);
});

test('script markup in a description is refused', () => {
  assert.match(messages(withEntry({ 'description.md': 'hi <script>alert(1)</script>' })), /MI105/);
});

// -------------------------------------------------------------- distribution

test('an entry needs somewhere to download from', () => {
  const { github, ...rest } = GOOD_META;
  assert.match(messages(withEntry({ 'meta.json': JSON.stringify(rest) })), /MI301/);
});

test('a downloadURL pointing at a page, not an archive, is refused', () => {
  const meta = { ...GOOD_META, downloadURL: 'https://github.com/ash/my_mod/releases/latest' };
  assert.match(messages(withEntry({ 'meta.json': JSON.stringify(meta) })), /MI303/);
});

test('release-asset and archive links are accepted', () => {
  for (const downloadURL of [
    'https://github.com/ash/my_mod/releases/latest/download/my_mod-1.0.0.zip',
    'https://github.com/ash/my_mod/releases/download/v1.0.0/my_mod-1.0.0.zip',
    'https://github.com/ash/my_mod/archive/refs/heads/main.zip',
  ]) {
    assert.deepEqual(withEntry({ 'meta.json': JSON.stringify({ ...GOOD_META, downloadURL }) }).errors, [], downloadURL);
  }
});

test('two folders cannot claim one mod id', () => {
  const collisions = checkCollisions([
    { folder: 'Ash@my_mod', meta: GOOD_META },
    { folder: 'Gary@my_mod', meta: { ...GOOD_META, author: 'Gary' } },
  ]);
  assert.match(collisions.join(), /MI203/);
});

// ----------------------------------------------------------------- downloads

const day = (n) => new Date(Date.UTC(2026, 0, 1 + n)).toISOString();

test('every zip asset in a release counts, source zipballs do not', () => {
  const byTag = zipDownloadsByTag([
    {
      tag_name: 'v1.1.0',
      assets: [
        { name: 'my_mod-1.1.0.zip', download_count: 40 },
        { name: 'my_mod-assets.zip', download_count: 2 },
        { name: 'notes.txt', download_count: 900 },
      ],
    },
    { tag_name: 'v1.0.0', assets: [] },
  ]);
  assert.deepEqual(byTag, { 'v1.1.0': 42 });
});

test('a re-uploaded asset cannot make a total go backwards', () => {
  const state = { version: 1, mods: {} };
  record(state, 'Ash@my_mod', { 'v1.0.0': 500 }, day(0));
  record(state, 'Ash@my_mod', { 'v1.0.0': 3 }, day(1));
  assert.equal(state.mods['Ash@my_mod'].total, 500);
});

test('tags that fall off the releases page keep their last known count', () => {
  const state = { version: 1, mods: {} };
  record(state, 'Ash@my_mod', { 'v1.0.0': 100 }, day(0));
  record(state, 'Ash@my_mod', { 'v1.1.0': 20 }, day(1));
  assert.equal(state.mods['Ash@my_mod'].total, 120);
});

test('history keeps one sample a day and expires past the retention window', () => {
  const state = { version: 1, mods: {} };
  record(state, 'Ash@my_mod', { 'v1.0.0': 1 }, day(0));
  record(state, 'Ash@my_mod', { 'v1.0.0': 2 }, '2026-01-01T18:00:00.000Z');
  assert.equal(state.mods['Ash@my_mod'].history.length, 1);
  record(state, 'Ash@my_mod', { 'v1.0.0': 3 }, day(40));
  assert.deepEqual(state.mods['Ash@my_mod'].history.map((s) => s.total), [3]);
});

test('recent is the delta against the newest sample outside the window', () => {
  const state = { version: 1, mods: {} };
  record(state, 'Ash@my_mod', { 'v1.0.0': 100 }, day(0));
  record(state, 'Ash@my_mod', { 'v1.0.0': 180 }, day(31));
  const summary = summarize(state.mods['Ash@my_mod'], day(31));
  assert.equal(summary.total, 180);
  assert.equal(summary.recent, 80);
  assert.equal(summary.window_days, 31);
});

test('one sample is not a window, so recent stays null rather than guessing', () => {
  const state = { version: 1, mods: {} };
  record(state, 'Ash@my_mod', { 'v1.0.0': 100 }, day(0));
  assert.deepEqual(summarize(state.mods['Ash@my_mod'], day(0)), {
    total: 100,
    recent: null,
    window_days: null,
    as_of: day(0),
  });
});

test('an entry with nothing to count summarizes to null, not zero', () => {
  assert.equal(summarize(undefined, day(0)), null);
});

test('retired folders are dropped from the accumulator', () => {
  const state = { version: 1, mods: {} };
  record(state, 'Ash@my_mod', { 'v1.0.0': 1 }, day(0));
  record(state, 'Gary@gone', { 'v1.0.0': 1 }, day(0));
  pruneDownloads(state, ['Ash@my_mod']);
  assert.deepEqual(Object.keys(state.mods), ['Ash@my_mod']);
});

// ------------------------------------------------------------------ markdown

test('descriptions are escaped, never injected', () => {
  const html = renderMarkdown('<script>alert(1)</script>');
  assert.ok(!html.includes('<script>'));
  assert.match(html, /&lt;script&gt;/);
});

test('javascript: links are defused', () => {
  assert.match(renderMarkdown('[x](javascript:alert(1))'), /href="#"/);
});

test('code spans survive the emphasis rules', () => {
  assert.match(renderMarkdown('use `snake_case_name` here'), /<code>snake_case_name<\/code>/);
});

test('lists, headings and fences render', () => {
  const html = renderMarkdown('## Title\n\n- one\n- two\n\n```\ncode\n```');
  assert.match(html, /<h3>Title<\/h3>/);
  assert.match(html, /<ul>\n<li>one<\/li>/);
  assert.match(html, /<pre><code>code<\/code><\/pre>/);
});
