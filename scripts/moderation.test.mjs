import { test } from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, writeFileSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { loadModeration, isQuarantined } from './lib/moderation.mjs';

test('moderation fails closed on corrupt state and distinguishes carts from mods', () => {
  const dir = mkdtempSync(join(tmpdir(), 'moderation-'));
  try {
    const file = join(dir, 'state.json');
    assert.deepEqual(loadModeration(file), {});
    writeFileSync(file, '{broken');
    assert.throws(() => loadModeration(file));
    writeFileSync(file, JSON.stringify({version: 1, entries: {'mods/a': {sha256: 'abc'}}}));
    const state = loadModeration(file);
    assert.equal(isQuarantined(state, 'mods', 'a'), true);
    assert.equal(isQuarantined(state, 'carts', 'a'), false);
  } finally { rmSync(dir, {recursive: true}); }
});
