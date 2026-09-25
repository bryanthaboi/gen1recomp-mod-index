"""
Configuration loader and validator for mod-scanner.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional
import yaml


@dataclass
class PretSource:
    name: str
    repo: str
    branch: str = "master"
    image_patterns: List[str] = field(default_factory=lambda: ["**/*.png"])


@dataclass
class MagicByteRule:
    name: str
    offset: int
    raw_bytes: bytes


@dataclass
class ArchiveConfig:
    max_unpacked_size_mb: int = 500
    max_file_count: int = 50000
    max_compression_ratio: float = 100.0

    @property
    def max_unpacked_size_bytes(self) -> int:
        return self.max_unpacked_size_mb * 1024 * 1024


@dataclass
class ContainedSignatureRule:
    name: str
    raw_bytes: bytes


@dataclass
class BinaryRules:
    blacklisted_extensions: List[str] = field(default_factory=list)
    magic_bytes: List[MagicByteRule] = field(default_factory=list)
    contained_signatures: List[ContainedSignatureRule] = field(default_factory=list)


@dataclass
class ImageRules:
    hash_type: str = "dhash"
    hash_size: int = 16
    threshold_auto_reject: int = 14
    threshold_flag_for_review: int = 30
    generate_diff_preview: bool = True
    preview_panel_size: int = 64


@dataclass
class DiscordConfig:
    token: str = ""
    guild_id: int = 0
    monitored_channel_ids: List[int] = field(default_factory=list)
    mod_review_channel_id: int = 0
    max_embed_items: int = 4
    attach_diff_bundle_zip: bool = True
    auto_delete_violations: bool = False


@dataclass
class PathsConfig:
    cache_dir: Path = field(default_factory=lambda: Path("./.cache"))
    whitelist_file: Path = field(default_factory=lambda: Path("./whitelist.json"))

    @property
    def reference_hashes_file(self) -> Path:
        return self.cache_dir / "reference_hashes.json"

    @property
    def reference_images_dir(self) -> Path:
        return self.cache_dir / "reference_images"


@dataclass
class ConcurrencyConfig:
    max_workers: int = 2


@dataclass
class Config:
    github_token: str = ""
    concurrency: ConcurrencyConfig = field(default_factory=ConcurrencyConfig)
    pret_sources: List[PretSource] = field(default_factory=list)
    archive: ArchiveConfig = field(default_factory=ArchiveConfig)
    binary_rules: BinaryRules = field(default_factory=BinaryRules)
    image_rules: ImageRules = field(default_factory=ImageRules)
    discord: DiscordConfig = field(default_factory=DiscordConfig)
    paths: PathsConfig = field(default_factory=PathsConfig)


    @classmethod
    def from_file(cls, config_path: str | Path = "config.yaml") -> Config:
        path = Path(config_path)
        raw_data: Dict[str, Any] = {}
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                raw_data = yaml.safe_load(f) or {}

        # Environment variable overrides
        github_token = os.environ.get("GITHUB_TOKEN", raw_data.get("github_token", ""))
        discord_token = os.environ.get("DISCORD_BOT_TOKEN", raw_data.get("discord", {}).get("token", ""))

        # Concurrency
        concurrency_data = raw_data.get("concurrency", {})
        concurrency = ConcurrencyConfig(
            max_workers=int(concurrency_data.get("max_workers", 2))
        )

        # Pret sources
        sources_data = raw_data.get("pret_sources", [])
        pret_sources = []
        for src in sources_data:
            pret_sources.append(
                PretSource(
                    name=src.get("name", "unknown"),
                    repo=src.get("repo", ""),
                    branch=src.get("branch", "master"),
                    image_patterns=src.get("image_patterns", ["**/*.png"]),
                )
            )

        # Archive
        arc_data = raw_data.get("archive", {})
        archive = ArchiveConfig(
            max_unpacked_size_mb=int(arc_data.get("max_unpacked_size_mb", 500)),
            max_file_count=int(arc_data.get("max_file_count", 50000)),
            max_compression_ratio=float(arc_data.get("max_compression_ratio", 100.0)),
        )

        # Binary rules
        bin_data = raw_data.get("binary_rules", {})
        exts = [e.lower() for e in bin_data.get("blacklisted_extensions", [])]
        magic_rules = []
        for m in bin_data.get("magic_bytes", []):
            hex_str = m.get("hex", "").replace(" ", "").strip()
            if hex_str:
                try:
                    raw_bytes = bytes.fromhex(hex_str)
                    magic_rules.append(
                        MagicByteRule(
                            name=m.get("name", "Unknown signature"),
                            offset=int(m.get("offset", 0)),
                            raw_bytes=raw_bytes,
                        )
                    )
                except ValueError:
                    pass

        contained_rules = []
        for c in bin_data.get("contained_signatures", []):
            raw_b = None
            if "hex" in c and c["hex"]:
                try:
                    raw_b = bytes.fromhex(c["hex"].replace(" ", "").strip())
                except ValueError:
                    pass
            elif "pattern" in c and c["pattern"]:
                raw_b = c["pattern"].encode("utf-8")

            if raw_b:
                contained_rules.append(
                    ContainedSignatureRule(
                        name=c.get("name", "Unknown contained signature"),
                        raw_bytes=raw_b,
                    )
                )

        binary_rules = BinaryRules(
            blacklisted_extensions=exts,
            magic_bytes=magic_rules,
            contained_signatures=contained_rules,
        )

        # Image rules
        img_data = raw_data.get("image_rules", {})
        thresholds = img_data.get("thresholds", {})
        image_rules = ImageRules(
            hash_type=img_data.get("hash_type", "dhash"),
            hash_size=int(img_data.get("hash_size", 16)),
            threshold_auto_reject=int(thresholds.get("auto_reject", 14)),
            threshold_flag_for_review=int(thresholds.get("flag_for_review", 30)),
            generate_diff_preview=bool(img_data.get("generate_diff_preview", True)),
            preview_panel_size=int(img_data.get("preview_panel_size", 64)),
        )

        # Discord
        disc_data = raw_data.get("discord", {})
        monitored_channels = [int(cid) for cid in disc_data.get("monitored_channel_ids", []) if cid]
        discord = DiscordConfig(
            token=discord_token,
            guild_id=int(os.environ.get("DISCORD_GUILD_ID", disc_data.get("guild_id", 0))),
            monitored_channel_ids=monitored_channels,
            mod_review_channel_id=int(os.environ.get("DISCORD_REVIEW_CHANNEL_ID", disc_data.get("mod_review_channel_id", 0))),
            max_embed_items=int(disc_data.get("max_embed_items", 4)),
            attach_diff_bundle_zip=bool(disc_data.get("attach_diff_bundle_zip", True)),
            auto_delete_violations=bool(disc_data.get("auto_delete_violations", False)),
        )

        # Paths
        paths_data = raw_data.get("paths", {})
        cache_dir = Path(paths_data.get("cache_dir", "./.cache"))
        whitelist_file = Path(paths_data.get("whitelist_file", "./whitelist.json"))
        paths = PathsConfig(cache_dir=cache_dir, whitelist_file=whitelist_file)

        return cls(
            github_token=github_token,
            concurrency=concurrency,
            pret_sources=pret_sources,
            archive=archive,
            binary_rules=binary_rules,
            image_rules=image_rules,
            discord=discord,
            paths=paths,
        )
