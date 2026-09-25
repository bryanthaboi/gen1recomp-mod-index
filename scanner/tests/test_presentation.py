import unittest
from presentation import sort_records, summary, progress_panel


class PresentationTests(unittest.TestCase):
    def test_numeric_sort_keeps_unknown_sizes_last_in_both_directions(self):
        records = [{'key': 'small', 'title': 'Small', 'status': 'clean', 'archive_bytes': 9},
                   {'key': 'large', 'title': 'Large', 'status': 'clean', 'archive_bytes': 100},
                   {'key': 'unknown', 'title': 'Unknown', 'status': 'incomplete'}]
        self.assertEqual([r['key'] for r in sort_records(records, 'zip')], ['small', 'large', 'unknown'])
        self.assertEqual([r['key'] for r in sort_records(records, 'zip', True)], ['large', 'small', 'unknown'])

    def test_summary_and_progress_escape_untrusted_names(self):
        self.assertIn('&lt;script&gt;', progress_panel({'done': 1, 'total': 2, 'entry': '<script>'}, True))
        self.assertNotIn('<script>', summary({'release': {'zip': {'name': '<script>'}}}))
