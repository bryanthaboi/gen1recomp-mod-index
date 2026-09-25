"""Conservative, source-only checks for Gen1Recomp mod API usage.

This module has no scanner dependencies so the same rules run in Pyodide.
The engine's modkit validator remains the authority for runtime/schema checks.
"""

from __future__ import annotations

import json
import posixpath
import re
from dataclasses import asdict, dataclass


MAX_SOURCE_BYTES = 16 * 1024 * 1024
MAX_MANIFEST_BYTES = 1024 * 1024
MAX_TOTAL_MANIFEST_BYTES = 4 * 1024 * 1024
SUPPORTED_REQUIRES = {"src.mods.Semver", "src.audio.ChipAsm", "src.pokemon.Stats"}
PERMISSIONS = {"network", "filesystem", "engine_internals", "steps", "background", "compute"}
REQUIRE_RE = re.compile(r'\brequire\s*\(?\s*["\'](src\.[\w.]+)["\']')
ALIAS_RE = re.compile(r'\b(?:local\s+)?([A-Za-z_]\w*)\s*=\s*require\s*\(?\s*["\'](src\.[\w.]+)["\']')
OVERRIDE_RE = re.compile(r'\bmod\.content\.([A-Za-z_]\w*)\s*:\s*override\s*\(')
LOVE_CALLBACK_RE = re.compile(
    r'\b(?:function\s+love\.(update|draw|keypressed|keyreleased|mousemoved|mousepressed|mousereleased|wheelmoved|gamepadpressed|gamepadreleased)\s*\('
    r'|love\.(update|draw|keypressed|keyreleased|mousemoved|mousepressed|mousereleased|wheelmoved|gamepadpressed|gamepadreleased)\s*=(?!=))'
)


@dataclass(frozen=True)
class ApiFinding:
    file_path: str
    line: int
    rule_id: str
    severity: str  # error or warning
    message: str
    suggestion: str

    def to_dict(self) -> dict:
        return asdict(self)


class ApiAnalyzer:
    """Check Lua files as they arrive and retain only bounded manifest data."""

    def __init__(self):
        self.files: dict[str, bytes] = {}
        self.names: set[str] = set()
        self.manifest_bytes = 0
        self.lua_candidates: dict[str, list[tuple[ApiFinding, str | None]]] = {}
        self.mod_entries: set[str] = set()

    def add_file(self, path: str, data: bytes | None = None):
        path = path.replace("\\", "/").lstrip("./")
        self.names.add(path)
        if data is None:
            return
        is_manifest = posixpath.basename(path) == "manifest.json"
        if is_manifest:
            if len(data) > MAX_MANIFEST_BYTES:
                return
            old_size = len(self.files.get(path, b""))
            if self.manifest_bytes - old_size + len(data) <= MAX_TOTAL_MANIFEST_BYTES:
                self.manifest_bytes += len(data) - old_size
                self.files[path] = data
            return
        if not path.endswith(".lua") or len(data) > MAX_SOURCE_BYTES:
            return
        source = data.decode("utf-8", "replace")
        self.lua_candidates[path] = self._check_lua(path, source)
        if posixpath.basename(path) == "main.lua":
            if re.search(r"return\s+function\s*\(\s*mod\s*\)", source):
                self.mod_entries.add(path)
            else:
                self.mod_entries.discard(path)

    def analyze(self) -> tuple[str, list[ApiFinding]]:
        findings: list[ApiFinding] = []
        manifests = sorted(p for p in self.names if posixpath.basename(p) == "manifest.json")
        manifest_roots = {posixpath.dirname(p) for p in manifests}
        checked = 0
        for manifest_path in manifests:
            prefix = posixpath.dirname(manifest_path)
            sibling = f"{prefix}/main.lua" if prefix else "main.lua"
            mod_entry = sibling in self.mod_entries
            raw = self.files.get(manifest_path)
            if raw is None:
                if not prefix or mod_entry:
                    checked += 1
                    findings.append(ApiFinding(manifest_path, 1, "API090", "warning",
                                               "Manifest was too large or unreadable; API checks were skipped for this mod.",
                                               "Keep manifest.json below 1 MiB and ensure it can be read."))
                continue
            try:
                manifest = json.loads(raw.decode("utf-8-sig"))
            except (UnicodeError, ValueError) as exc:
                if mod_entry:
                    checked += 1
                    findings.append(ApiFinding(manifest_path, 1, "API001", "error",
                                               f"Manifest is not valid JSON: {exc}", "Fix manifest.json syntax."))
                continue
            if not isinstance(manifest, dict):
                if mod_entry:
                    checked += 1
                    findings.append(ApiFinding(manifest_path, 1, "API001", "error",
                                               "Manifest must be a JSON object.", "Use a JSON object with id, name, version and entry."))
                continue
            if not ("entry" in manifest or ("id" in manifest and "api" in manifest) or mod_entry):
                continue
            checked += 1
            findings.extend(self._check_manifest(manifest_path, manifest))
            permissions = manifest.get("permissions")
            grants = {p for p in permissions if isinstance(p, str)} if isinstance(permissions, list) else set()
            for path in self.names - self.files.keys() - self.lua_candidates.keys():
                if not path.endswith(".lua") or (prefix and not path.startswith(prefix + "/")):
                    continue
                if any(other and other != prefix and path.startswith(other + "/")
                       for other in manifest_roots):
                    continue
                relative = path[len(prefix) + 1:] if prefix else path
                if any(part in {"tests", "test", "tools", "vendor"} for part in relative.split("/")):
                    continue
                findings.append(ApiFinding(path, 1, "API090", "warning",
                                           "Lua source was too large or unreadable; API checks were skipped for this file.",
                                           "Keep individual source files below 16 MiB and ensure they can be read."))
            for path, candidates in self.lua_candidates.items():
                if prefix and not path.startswith(prefix + "/"):
                    continue
                if any(other and other != prefix and path.startswith(other + "/")
                       for other in manifest_roots):
                    continue
                relative = path[len(prefix) + 1:] if prefix else path
                if any(part in {"tests", "test", "tools", "vendor"} for part in relative.split("/")):
                    continue
                findings.extend(finding for finding, required in candidates if required is None or required not in grants)
        if not checked and not manifests:
            for path in self.mod_entries:
                findings.append(ApiFinding(path, 1, "API000", "error",
                                           "Mod entry has no manifest.json beside it.",
                                           "Add a manifest.json with id, name, version and entry."))
                checked += 1
        findings.sort(key=lambda f: (f.file_path, f.line, f.rule_id))
        if not checked:
            return "NOT_APPLICABLE", findings
        return ("ISSUES" if findings else "OK"), findings

    def _check_manifest(self, path: str, manifest: dict) -> list[ApiFinding]:
        findings = []

        def add(field: str, rule: str, message: str, suggestion: str, severity: str = "error"):
            source = self.files[path].decode("utf-8-sig", "replace")
            match = re.search(r'"' + re.escape(field) + r'"\s*:', source)
            line = source.count("\n", 0, match.start()) + 1 if match else 1
            findings.append(ApiFinding(path, line, rule, severity, message, suggestion))

        for field in ("id", "name", "version", "entry"):
            if not isinstance(manifest.get(field), str) or not manifest[field]:
                add(field, "API002", f"Required manifest field '{field}' is missing or empty.",
                    f"Set '{field}' to a non-empty string.")
        entry = manifest.get("entry")
        if isinstance(entry, str) and entry:
            clean = posixpath.normpath(entry.replace("\\", "/"))
            if entry.startswith(("/", "\\")) or clean == ".." or clean.startswith("../"):
                add("entry", "API003", "Entry path leaves the mod directory.",
                    "Use a relative path inside this mod.")
            else:
                prefix = posixpath.dirname(path)
                full_entry = posixpath.join(prefix, clean) if prefix else clean
                if full_entry not in self.names:
                    add("entry", "API004", f"Entry file '{entry}' is absent from the scanned mod.",
                        "Include the entry file or correct the manifest path.")
        api = manifest.get("api", 1)
        try:
            api_number = float(api) if not isinstance(api, bool) else None
        except (TypeError, ValueError, OverflowError):
            api_number = None
        if api_number is None or not api_number.is_integer() or not 1 <= api_number <= 2:
            add("api", "API005", f"Unsupported mod API version {api!r}; this checker targets API 1 and 2.",
                "Use a supported API version, or validate against a newer engine.")
        permissions = manifest.get("permissions", [])
        if not isinstance(permissions, list) or any(not isinstance(p, str) for p in permissions):
            add("permissions", "API006", "Permissions must be a list of names.",
                "Use a JSON array of permission strings.")
        else:
            for permission in sorted(set(permissions) - PERMISSIONS):
                add("permissions", "API006", f"Unknown permission '{permission}'.",
                    "Use a permission supported by the engine manifest.",
                    severity="error" if api_number == 2 else "warning")
        return findings

    @staticmethod
    def _check_lua(path: str, source: str) -> list[tuple[ApiFinding, str | None]]:
        findings: list[tuple[ApiFinding, str | None]] = []
        aliases: dict[str, str] = {}
        for number, line in enumerate(source.splitlines(), 1):
            # Strip ordinary Lua line comments; do not claim to parse all Lua syntax.
            code = line.split("--", 1)[0]
            for match in REQUIRE_RE.finditer(code):
                module = match.group(1)
                permission = "network" if module.startswith("src.link.") else "engine_internals"
                if module not in SUPPORTED_REQUIRES:
                    findings.append((ApiFinding(path, number, "API010", "warning",
                                                f"'{module}' requires the '{permission}' manifest permission.",
                                                f"Declare '{permission}', or use the public mod API instead."), permission))
            alias = ALIAS_RE.search(code)
            if alias:
                aliases[alias.group(1)] = alias.group(2)
            for match in OVERRIDE_RE.finditer(code):
                findings.append((ApiFinding(path, number, "API020", "warning",
                                            f"Whole-record override of '{match.group(1)}' may erase another mod's fields.",
                                            "For record registries, use :patch for partial changes; keep :override for intentional full replacement."), None))
            callback = LOVE_CALLBACK_RE.search(code)
            if callback:
                findings.append((ApiFinding(path, number, "API022", "warning",
                                            f"Legacy love.{callback.group(1) or callback.group(2)} assignment can replace another mod's callback.",
                                            "Use mod.hooks:wrap or mod.events:on for supported behavior."), None))
            for name, module in aliases.items():
                direct_write = re.search(r'\b' + re.escape(name) + r'(?:\.[A-Za-z_]\w*|\[[^]]+\])\s*=(?!=)', code)
                function_write = re.search(r'\bfunction\s+' + re.escape(name) + r'\.[A-Za-z_]\w*\s*\(', code)
                if direct_write or function_write:
                    findings.append((ApiFinding(path, number, "API021", "warning",
                                                f"Direct mutation of '{module}' bypasses mod-owned hooks and rollback.",
                                                "Use mod.content, mod.hooks:wrap, or mod.events:on where supported."), None))
        return findings
