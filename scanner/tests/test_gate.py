import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import cli


class GateTests(unittest.TestCase):
    def run_gate(self, statuses, approved=False, watchlist=None):
        tmp = tempfile.TemporaryDirectory(); self.addCleanup(tmp.cleanup)
        root = Path(tmp.name); feed = root / 'index.json'
        original = {'mods': [{'folder': str(n), 'title': str(n)} for n in range(len(statuses))], 'carts': []}
        feed.write_text(json.dumps(original))
        records = [{'key': f'mods/{n}', 'status': status, 'sha256': str(n), 'complete': status != 'incomplete', 'api': []}
                   for n, status in enumerate(statuses)]
        with patch('sys.argv', ['cli', '--gate-index', str(feed), '--output', str(root / 'report.json')]), \
             patch('cli.Engine'), patch('cli.local_entries', return_value=[]), \
             patch('cli.json_get', return_value={'approvals': {'mods/0': {'sha256': '0'}} if approved else {}, 'entries': {}, 'watchlist': watchlist or {}}), \
             patch('cli.scan_entry', side_effect=records):
            code = cli.main()
        return code, json.loads(feed.read_text()), original

    def test_quarantine_excluded_and_counts_updated(self):
        code, feed, _ = self.run_gate(['quarantined', 'clean'])
        self.assertEqual(code, 0)
        self.assertEqual(feed['mods'], [{'folder': '1', 'title': '1'}])
        self.assertEqual(feed['count'], 1)

    def test_trusted_artifact_approval_restores_listing(self):
        code, feed, _ = self.run_gate(['quarantined'], approved=True)
        self.assertEqual(code, 0); self.assertEqual(feed['count'], 1)

    def test_mass_incomplete_scan_preserves_existing_feed(self):
        code, feed, original = self.run_gate(['incomplete'] * 6)
        self.assertEqual(code, 1); self.assertEqual(feed, original)

    def test_clean_update_of_quarantined_listing_stays_out_until_approved(self):
        held = {'mods/0': {'sha256': 'previous'}}
        code, feed, _ = self.run_gate(['clean'], watchlist=held)
        self.assertEqual(code, 0); self.assertEqual(feed['count'], 0)
        code, feed, _ = self.run_gate(['clean'], approved=True, watchlist=held)
        self.assertEqual(code, 0); self.assertEqual(feed['count'], 1)
