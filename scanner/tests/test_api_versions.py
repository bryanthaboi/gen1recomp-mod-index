import json
import unittest

from vendor.api_scanner import ApiAnalyzer


class ApiVersionTests(unittest.TestCase):
    def findings(self, api, permissions=None, source="return function(mod) end"):
        analyzer = ApiAnalyzer()
        manifest = {"id": "api_test", "name": "API test", "version": "1.0.0",
                    "entry": "main.lua", "api": api, "permissions": permissions or []}
        analyzer.add_file("manifest.json", json.dumps(manifest).encode())
        analyzer.add_file("main.lua", source.encode())
        return analyzer.analyze()[1]

    def test_supported_api_versions_remain_installable(self):
        for api in (1, 2, 3):
            with self.subTest(api=api):
                self.assertEqual(self.findings(api), [])

    def test_unknown_and_malformed_api_versions_stay_blocked(self):
        for api in (0, 4, 1.5, True, None, "invalid"):
            with self.subTest(api=api):
                errors = [f for f in self.findings(api) if f.severity == "error"]
                self.assertIn("API005", [f.rule_id for f in errors])

    def test_api3_keeps_strict_permission_validation(self):
        for api in (2, 3):
            with self.subTest(api=api):
                findings = self.findings(api, ["invented_permission"])
                self.assertTrue(any(f.rule_id == "API006" and f.severity == "error"
                                    for f in findings))
        self.assertTrue(any(f.rule_id == "API006" and f.severity == "warning"
                            for f in self.findings(1, ["invented_permission"])))

    def test_api3_keeps_missing_permission_findings(self):
        source = 'local Game = require("src.core.Game")\nreturn function(mod) end'
        self.assertTrue(any(f.rule_id == "API010" for f in self.findings(3, source=source)))
        self.assertEqual(self.findings(3, ["engine_internals"], source), [])


if __name__ == "__main__":
    unittest.main()
