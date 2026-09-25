"""
Binary scanner for detecting console ROM headers and blacklisted extensions.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import BinaryIO, Optional
from ..config import BinaryRules, MagicByteRule


@dataclass
class BinaryViolation:
    filename: str
    rule_name: str
    reason: str


TEXT_SOURCE_EXTENSIONS = {
    ".lua", ".py", ".md", ".txt", ".json", ".yml", ".yaml",
    ".toml", ".ini", ".c", ".h", ".cpp", ".hpp", ".rs", ".go", ".js", ".ts", ".html", ".css",
    ".patch", ".diff", ".log", ".csv", ".tsv", ".xml", ".svg", ".card"
}


def check_file_stream_for_magic(
    stream: BinaryIO,
    filename: str,
    rules: BinaryRules,
    chunk_size: int = 65536,  # 64 KB chunk for deep package scanning
) -> Optional[BinaryViolation]:
    """
    Scans the beginning chunk of a stream for known console magic bytes,
    checks binary packages for contained proprietary signatures,
    and verifies filename extensions against blacklists.
    Does NOT load entire files into memory.
    """
    # 1. Check extension blacklist
    _, ext = os.path.splitext(filename)
    ext_lower = ext.lower()
    if ext_lower in rules.blacklisted_extensions:
        return BinaryViolation(
            filename=filename,
            rule_name="Blacklisted Extension",
            reason=f"File '{filename}' has a prohibited console ROM/container extension '{ext_lower}'",
        )

    # 2. Read the header chunk for signature verification
    header_chunk = stream.read(chunk_size)
    if not header_chunk:
        return None

    header_len = len(header_chunk)

    # 3. Check fixed-offset console magic byte rules
    for rule in rules.magic_bytes:
        req_len = rule.offset + len(rule.raw_bytes)
        if header_len >= req_len:
            extracted = header_chunk[rule.offset : req_len]
            if extracted == rule.raw_bytes:
                return BinaryViolation(
                    filename=filename,
                    rule_name=rule.name,
                    reason=f"File '{filename}' matches console ROM header signature '{rule.name}' at offset 0x{rule.offset:04X}",
                )

    # 4. Check contained signatures for binary packages / non-text files
    if ext_lower not in TEXT_SOURCE_EXTENSIONS and rules.contained_signatures:
        for c_rule in rules.contained_signatures:
            pos = header_chunk.find(c_rule.raw_bytes)
            if pos != -1:
                return BinaryViolation(
                    filename=filename,
                    rule_name=c_rule.name,
                    reason=f"Binary package '{filename}' contains prohibited proprietary asset signature '{c_rule.name}' at byte offset {pos}",
                )

    return None
