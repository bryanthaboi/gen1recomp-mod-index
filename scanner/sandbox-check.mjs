// Reuse the existing index sandbox rules without executing mod Lua.
import { readFileSync } from 'node:fs';
import { scanFiles } from '../scripts/lib/lua-scan.mjs';
const input = JSON.parse(readFileSync(0, 'utf8'));
process.stdout.write(JSON.stringify(scanFiles(input.files, input.permissions)));
