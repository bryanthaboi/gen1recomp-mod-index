import { readFileSync } from 'node:fs';

export function loadModeration(path) {
  try {
    const doc = JSON.parse(readFileSync(path, 'utf8'));
    if (doc.version !== 1 || !doc.entries || typeof doc.entries !== 'object' || Array.isArray(doc.entries)) {
      throw new Error('Invalid moderation state');
    }
    return doc.entries;
  } catch (error) {
    if (error.code === 'ENOENT') return {};
    throw error; // Never publish a broken policy document as an empty quarantine.
  }
}

export function isQuarantined(entries, root, folder) {
  return Object.hasOwn(entries, `${root}/${folder}`);
}
