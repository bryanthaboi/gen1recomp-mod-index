import io
import json
from pathlib import Path
import tempfile
import unittest
import zipfile
from unittest.mock import patch

from PIL import Image
from engine import Engine, POLICY, build_references, redact, public_url
from store import Store
from catalog import release_for
from cart import parse_bundle


def archive(files):
    out = io.BytesIO()
    with zipfile.ZipFile(out, 'w') as z:
        for name, data in files.items(): z.writestr(name, data)
    return out.getvalue()


class ScannerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        image = Image.new('RGBA', (32, 32))
        for x in range(32):
            for y in range(32): image.putpixel((x, y), ((x * 13) % 256, (y * 17) % 256, (x * y) % 256, 255))
        self.image = image
        image.save(self.root / 'sprite.png')
        build_references(self.root, self.root / 'references.json')
        self.engine = Engine(self.root / 'references.json', self.root, {**POLICY, 'auto_quarantine_exact': 2})

    def test_duplicate_assets_do_not_inflate_unique_count(self):
        raw = (self.root / 'sprite.png').read_bytes()
        result = self.engine.scan(archive({'a.png': raw, 'b.png': raw}))
        self.assertEqual(result['exact_unique'], 1)
        self.assertEqual(result['status'], 'review')
        self.assertTrue(result['previews'])

    def test_oversized_manifest_keeps_inventory_and_exact_size(self):
        engine = Engine(self.root / 'references.json', self.root, {**POLICY, 'max_member_bytes': 64})
        data = archive({'manifest.json': b'x' * 100, 'readme.txt': b'hello'})
        result = engine.scan(data)
        self.assertFalse(result['complete'])
        self.assertEqual(result['archive_bytes'], len(data))
        self.assertEqual(result['unpacked_bytes'], 105)
        self.assertEqual(result['total_files'], 2)
        self.assertEqual(result['file_stats'][0]['bytes'], 100)
        self.assertTrue(result['file_stats'][0]['over_member_limit'])
        self.assertIn('100 bytes', ' '.join(result['errors']))

    def test_incomplete_download_can_be_manually_quarantined_but_not_approved(self):
        store = Store(self.root / 'large.sqlite')
        scan_id = store.record({'key': 'mods/large', 'sha256': '', 'checked_at': 1, 'status': 'incomplete', 'complete': False})
        store.decide(scan_id, 'quarantine', 'oversized download')
        self.assertIn('mods/large', store.quarantine_manifest()['entries'])
        with self.assertRaises(ValueError): store.decide(scan_id, 'approve', 'cannot inspect')

    def test_distinct_exact_assets_cross_quarantine_threshold(self):
        other = self.image.copy(); other.putpixel((0, 0), (255, 0, 0, 255))
        other.save(self.root / 'other.png')
        build_references(self.root, self.root / 'references.json')
        engine = Engine(self.root / 'references.json', self.root, {**POLICY, 'auto_quarantine_exact': 2})
        result = engine.scan(archive({p.name: p.read_bytes() for p in self.root.glob('*.png')}))
        self.assertEqual(result['exact_unique'], 2)
        self.assertEqual(result['status'], 'quarantined')

    def test_same_perceptual_hash_is_not_exact(self):
        image = self.image.copy()
        image.putpixel((0, 0), (1, 1, 1, 255))
        out = io.BytesIO(); image.save(out, format='PNG')
        result = self.engine.scan(archive({'a.png': out.getvalue()}))
        self.assertEqual(result['exact_unique'], 0)
        self.assertEqual(result['status'], 'review')

    def test_path_traversal_and_corrupt_images_are_incomplete(self):
        for files in ({'../a.lua': 'hi'}, {'a.png': 'invalid'}):
            result = self.engine.scan(archive(files))
            self.assertFalse(result['complete'])
            self.assertEqual(result['status'], 'incomplete')

    def test_invalid_manifest_fails_api(self):
        result = self.engine.scan(archive({'manifest.json': '{broken', 'main.lua': 'return function(mod) end'}))
        self.assertTrue(any(f['severity'] == 'error' for f in result['api']))

    def test_existing_sandbox_errors_are_preserved(self):
        result = self.engine.scan(archive({'main.lua': 'local io = require("io")'}))
        self.assertTrue(any(f['rule_id'] == 'SANDBOX' and f['severity'] == 'error' for f in result['api']))

    def test_extension_is_only_review(self):
        result = self.engine.scan(archive({'fake.gb': b'not a rom'}))
        self.assertEqual(result['status'], 'review')
        self.assertEqual(result['assets'][0]['kind'], 'binary_review')

    def test_long_console_signature_quarantines(self):
        rule = next(r for r in self.engine.config.binary_rules.magic_bytes if len(r.raw_bytes) >= 16)
        raw = bytearray(1024)
        raw[rule.offset:rule.offset + len(rule.raw_bytes)] = rule.raw_bytes
        result = self.engine.scan(archive({'renamed.dat': raw}))
        self.assertEqual(result['status'], 'quarantined')

    def test_redaction(self):
        text = redact('/Users/somebody/work /home/person/foo https://api.pushcut.io/secret/notifications/test ghp_abcdef')
        self.assertNotIn('somebody', text); self.assertNotIn('person', text); self.assertNotIn('/secret/', text)
        self.assertNotIn('ghp_', text)

    def test_private_download_refused(self):
        with self.assertRaises(ValueError): public_url('https://127.0.0.1/secrets')

    def test_approval_is_artifact_specific_and_outage_preserves_quarantine(self):
        store = Store(self.root / 'db.sqlite')
        record = {'key': 'mods/a', 'sha256': 'one', 'checked_at': 1, 'status': 'quarantined', 'complete': True}
        scan_id = store.record(record)
        self.assertIn('mods/a', store.quarantine_manifest()['entries'])
        store.record({**record, 'sha256': '', 'status': 'incomplete', 'complete': False})
        self.assertIn('mods/a', store.quarantine_manifest()['entries'])
        store.decide(scan_id, 'approve', 'reviewed')
        self.assertEqual(store.effective(record)['status'], 'approved')
        self.assertEqual(store.effective({**record, 'sha256': 'two'})['status'], 'updated_recheck')

    def test_notifications_are_deduplicated(self):
        store = Store(self.root / 'db.sqlite')
        store.enqueue('a', {'title': 'one'}); store.enqueue('a', {'title': 'one'})
        self.assertEqual(len(store.pending()), 1)
        store.delivery('a', True)
        store.enqueue('a', {'title': 'one'})
        self.assertEqual(store.pending(), [])

    def test_quarantined_update_requires_explicit_approval_and_future_updates_recheck(self):
        store = Store(self.root / 'sticky.sqlite')
        original = {'key': 'mods/a', 'sha256': 'one', 'checked_at': 1, 'status': 'quarantined', 'complete': True}
        store.record(original)
        updated = {**original, 'sha256': 'two', 'status': 'clean'}
        scan_id = store.record(updated)
        self.assertEqual(store.latest()[0]['status'], 'updated_recheck')
        self.assertIn('mods/a', store.quarantine_manifest()['entries'])
        store = Store(self.root / 'sticky.sqlite')
        self.assertEqual(store.latest()[0]['status'], 'updated_recheck')
        store.decide(scan_id, 'approve', 'new version reviewed')
        self.assertEqual(store.latest()[0]['status'], 'approved')
        self.assertNotIn('mods/a', store.quarantine_manifest()['entries'])
        self.assertIn('mods/a', store.quarantine_manifest()['watchlist'])
        store.record({**updated, 'sha256': 'three'})
        self.assertEqual(store.latest()[0]['status'], 'updated_recheck')
        store.decide(scan_id, 'reset', 'reset old approval')
        self.assertIn('mods/a', store.quarantine_manifest()['entries'])

    def test_untrusted_ci_cannot_create_quarantine_history(self):
        store = Store(self.root / 'ci.sqlite')
        store.record({'key': 'mods/a', 'sha256': 'one', 'checked_at': 1, 'status': 'quarantined'}, origin='ci')
        self.assertEqual(Store(self.root / 'ci.sqlite').quarantine_manifest()['watchlist'], {})

    def test_incomplete_scans_never_notify(self):
        from notify import needs_notification
        for status in ('incomplete', 'quarantined', 'updated_recheck', 'review'):
            self.assertFalse(needs_notification({'status': status, 'complete': False, 'priority': True}))
        self.assertTrue(needs_notification({'status': 'updated_recheck', 'complete': True}))

    def test_database_backup_retains_history(self):
        store = Store(self.root / 'db.sqlite')
        store.record({'key': 'mods/a', 'sha256': 'one', 'checked_at': 1, 'status': 'clean', 'complete': True})
        store.backup(self.root / 'backup.sqlite')
        self.assertEqual(Store(self.root / 'backup.sqlite').latest()[0]['key'], 'mods/a')

    def test_fixed_release_is_respected(self):
        releases = [{'tag_name': 'v1.0.0', 'assets': [{'name': 'm-1.0.0.zip', 'browser_download_url': 'https://example.com/old'}]},
                    {'tag_name': 'v2.0.0', 'assets': [{'name': 'm-2.0.0.zip', 'browser_download_url': 'https://example.com/new'}]}]
        with patch('catalog.json_get', return_value=releases):
            result = release_for({'github': 'a/b', 'id': 'm', 'fixed_release_tag': 'v1.0.0'})
        self.assertEqual(result['version'], '1.0.0')

    def test_cart_is_data_and_cannot_execute_code(self):
        bundle = parse_bundle(b'return {format="g1rcart", formatVersion=1, cart={mods={[1]={id="a", options={enabled=true}},},},}')
        self.assertEqual(bundle['cart']['mods'][0]['id'], 'a')
        for text in [b'return {format="g1rcart",formatVersion=1,cart={}} os.execute("bad")',
                     b'return {format="g1rcart",formatVersion=1,cart={x=load("bad")}}']:
            with self.assertRaises(ValueError): parse_bundle(text)


if __name__ == '__main__': unittest.main()
