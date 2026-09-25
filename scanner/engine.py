"""Bounded, source-only release inspection. Never imports or runs mod code."""
from __future__ import annotations

import base64
import hashlib
import io
import ipaddress
import json
import os
from pathlib import Path, PurePosixPath
import re
import socket
import subprocess
import time
from urllib.parse import urlsplit, urljoin
import warnings
import zipfile

import requests
from PIL import Image
from vendor.api_scanner import ApiAnalyzer
from vendor.config import Config
from vendor.core.binary_scanner import check_file_stream_for_magic
from vendor.core.image_scanner import compute_image_hash, generate_diff_preview

ROOT = Path(__file__).resolve().parent
POLICY = json.loads((ROOT / 'policy.json').read_text())
VERSION = '1'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def redact(value):
    text = str(value)
    text = re.sub(r'/(?:Users|home)/[^/\s"\']+', '/user', text)
    text = re.sub(r'https://api\.pushcut\.io/[^/\s]+', 'https://api.pushcut.io/REDACTED', text)
    text = re.sub(r'\b(?:gh[pousr]_[A-Za-z0-9_]+|github_pat_[A-Za-z0-9_]+)\b', '[REDACTED]', text)
    return re.sub(r'[\x00-\x08\x0b-\x1f\x7f]', '', text)


def public_url(url):
    parsed = urlsplit(url)
    if parsed.scheme != 'https' or not parsed.hostname or parsed.username or parsed.password or parsed.port not in (None, 443):
        raise ValueError('Only public HTTPS downloads are allowed')
    addresses = socket.getaddrinfo(parsed.hostname, 443, type=socket.SOCK_STREAM)
    if not addresses or any(not ipaddress.ip_address(row[4][0]).is_global for row in addresses):
        raise ValueError('Nonpublic download address refused')
    return url


def fetch(url, limit=POLICY['max_download_bytes'], token='', timeout=90):
    """Cap streamed bytes, wall time, redirects; never forward auth to downloads."""
    start = time.monotonic()
    for _ in range(6):
        public_url(url)
        headers = {'User-Agent': 'gen1mod-review', 'Accept': 'application/vnd.github+json'}
        if token and urlsplit(url).hostname == 'api.github.com':
            headers['Authorization'] = f'Bearer {token}'
        with requests.get(url, headers=headers, stream=True, timeout=(15, 30), allow_redirects=False) as response:
            if response.is_redirect:
                url = urljoin(url, response.headers['Location'])
                continue
            response.raise_for_status()
            if int(response.headers.get('Content-Length', 0)) > limit:
                raise ValueError('Download exceeds byte limit')
            chunks, size = [], 0
            for chunk in response.iter_content(65536):
                size += len(chunk)
                if size > limit or time.monotonic() - start > timeout:
                    raise ValueError('Download exceeds byte or time limit')
                chunks.append(chunk)
            return b''.join(chunks)
    raise ValueError('Too many redirects')


def json_get(url, token=''):
    return json.loads(fetch(url, 16 * 1024 * 1024, token))


def pixel_digest(img):
    rgba = img.convert('RGBA')
    # Preserve dimensions and RGBA values: no resizing or perceptual equivalence.
    return digest(f'{rgba.width}x{rgba.height}:'.encode() + rgba.tobytes())


def build_references(directory, output):
    refs = []
    for path in sorted(Path(directory).rglob('*.png')):
        with Image.open(path) as img:
            img.load()
            if min(img.size) < 16 or img.convert('L').getextrema()[0] == img.convert('L').getextrema()[1]:
                continue
            refs.append({'path': path.relative_to(directory).as_posix(), 'pixel_sha256': pixel_digest(img),
                         'file_sha256': digest(path.read_bytes()), 'dhash': compute_image_hash(img)})
    Path(output).write_text(json.dumps({'version': 1, 'references': refs}, separators=(',', ':')) + '\n')
    return len(refs)


class Engine:
    def __init__(self, references=None, images=None, policy=None):
        self.policy = policy or POLICY
        path = Path(references or ROOT / 'references.json')
        raw = path.read_bytes()
        self.refs = json.loads(raw)['references']
        if not self.refs:
            raise ValueError('Reference database is empty')
        self.exact = {r['pixel_sha256']: r for r in self.refs}
        self.hashes = [(int(r['dhash'], 16), r) for r in self.refs]
        self.images = Path(images or os.environ.get('REFERENCE_IMAGES', '/references'))
        code = b''.join(p.read_bytes() for p in sorted(ROOT.rglob('*.py')) if '__pycache__' not in str(p))
        sandbox = (ROOT.parent / 'scripts/lib/lua-scan.mjs').read_bytes()
        self.revision = digest(raw + json.dumps(self.policy, sort_keys=True).encode() + code + sandbox + (ROOT / 'sandbox-check.mjs').read_bytes() + (ROOT / 'upstream-config.yaml').read_bytes())
        self.config = Config.from_file(ROOT / 'upstream-config.yaml')
        Image.MAX_IMAGE_PIXELS = self.policy['max_image_pixels']

    def scan(self, data):
        result = {'sha256': digest(data), 'scanner': self.revision, 'status': 'clean', 'complete': True,
                  'files': 0, 'images': 0, 'exact_unique': 0, 'similar_unique': 0,
                  'assets': [], 'api': [], 'errors': [], 'previews': []}
        analyzer = ApiAnalyzer()
        exact, similar = set(), set()
        started = time.monotonic()
        source_bytes = 0
        lua_files = []

        def incomplete(message):
            result['complete'] = False
            if len(result['errors']) < 100:
                result['errors'].append(redact(message))

        def inspect_image(raw, label):
            try:
                with warnings.catch_warnings():
                    warnings.simplefilter('error', Image.DecompressionBombWarning)
                    img = Image.open(io.BytesIO(raw))
                    if img.width * img.height > self.policy['max_image_pixels']:
                        raise ValueError('Image pixel limit exceeded')
                    img.load()
                result['images'] += 1
                if min(img.size) < 16 or img.convert('L').getextrema()[0] == img.convert('L').getextrema()[1]:
                    return
                ph = pixel_digest(img)
                ref = self.exact.get(ph)
                distance = 0
                if ref:
                    kind = 'exact_pixels'
                    exact.add(ph)
                else:
                    h = int(compute_image_hash(img), 16)
                    distance, ref = min((((h ^ rh).bit_count(), r) for rh, r in self.hashes), key=lambda pair: pair[0])
                    if distance > self.policy['similarity_distance']:
                        return
                    kind = 'similarity'
                    similar.add(ph)
                finding = {'path': label, 'kind': kind, 'reference': ref['path'], 'distance': distance, 'pixel_sha256': ph}
                result['assets'].append(finding)
                if len(result['previews']) < self.policy['max_previews']:
                    path = self.images / ref['path']
                    if path.is_file() and digest(path.read_bytes()) == ref['file_sha256']:
                        with Image.open(path) as reference:
                            # Bound preview dimensions even for giant supplied images.
                            preview_mod = img.copy(); preview_ref = reference.copy()
                            preview_mod.thumbnail((256, 256), Image.Resampling.NEAREST)
                            preview_ref.thumbnail((256, 256), Image.Resampling.NEAREST)
                            preview = generate_diff_preview(preview_mod, preview_ref)
                            out = io.BytesIO(); preview.save(out, format='PNG')
                        result['previews'].append({'path': label, 'reference': ref['path'], 'image': base64.b64encode(out.getvalue()).decode()})
            except Exception:
                incomplete(f'Image could not be fully checked: {label}')

        try:
            if len(data) > self.policy['max_download_bytes']:
                raise ValueError('Archive download limit exceeded')
            with zipfile.ZipFile(io.BytesIO(data)) as archive:
                infos = archive.infolist()
                if len(infos) > self.policy['max_files'] or sum(i.file_size for i in infos) > self.policy['max_unpacked_bytes']:
                    raise ValueError('Archive file count or unpacked size limit exceeded')
                names = set()
                for info in infos:
                    name = info.filename.replace('\\', '/')
                    path = PurePosixPath(name)
                    if path.is_absolute() or '..' in path.parts or re.match(r'^[A-Za-z]:', name) or name in names or (info.external_attr >> 16) & 0o170000 == 0o120000:
                        raise ValueError('Archive contains unsafe or duplicate paths')
                    names.add(name)
                    if info.is_dir():
                        continue
                    if time.monotonic() - started > self.policy['max_seconds']:
                        raise ValueError('Scan time limit exceeded')
                    result['files'] += 1
                    analyzer.add_file(name)
                    if info.file_size > self.policy['max_member_bytes']:
                        incomplete(f'File exceeds scan limit: {name}')
                        continue
                    raw = archive.read(info)
                    if len(raw) > self.policy['max_member_bytes']:
                        raise ValueError('Expanded member exceeds scan limit')
                    ext = path.suffix.lower()
                    if ext == '.lua' or path.name == 'manifest.json':
                        source_bytes += len(raw)
                        if len(raw) <= 16 * 1024 * 1024 and source_bytes <= 32 * 1024 * 1024:
                            analyzer.add_file(name, raw)
                            if ext == '.lua': lua_files.append({'name': name, 'text': raw.decode('utf-8', 'replace')})
                        else:
                            incomplete(f'Source budget exceeded: {name}')
                    binary = check_file_stream_for_magic(io.BytesIO(raw), name, self.config.binary_rules)
                    if binary:
                        # An extension or four-byte marker alone is not proof of a ROM.
                        strong = len(raw) >= 512 and any(len(rule.raw_bytes) >= 16 and raw[rule.offset:rule.offset + len(rule.raw_bytes)] == rule.raw_bytes
                                     for rule in self.config.binary_rules.magic_bytes)
                        result['assets'].append({'path': name, 'kind': 'rom_signature' if strong else 'binary_review', 'message': binary.reason})
                    if ext in {'.png', '.jpg', '.jpeg', '.bmp', '.webp', '.tga'}:
                        inspect_image(raw, name)
                    elif ext in {'.rgba', '.rgb', '.bgra', '.raw'}:
                        import math
                        channels = 3 if ext == '.rgb' else 4
                        width = math.isqrt(len(raw) // channels)
                        if width and width * width * channels == len(raw):
                            img = Image.frombytes('RGB' if channels == 3 else 'RGBA', (width, width), raw,
                                                  'raw', 'BGRA' if ext == '.bgra' else ('RGB' if channels == 3 else 'RGBA'))
                            out = io.BytesIO(); img.save(out, format='PNG'); inspect_image(out.getvalue(), name)
                        else:
                            incomplete(f'Unknown raw image dimensions: {name}')
                    elif ext in {'.zip', '.7z', '.rar', '.gz'}:
                        incomplete(f'Nested archive requires review: {name}')
                    elif ext in {'.pack', '.dat', '.pak', '.bundle', '.bin', '.arc', '.res', '.fsys', '.rarc'}:
                        offset, count = 0, 0
                        while count < 100:
                            begin = raw.find(b'\x89PNG\r\n\x1a\n', offset)
                            if begin < 0:
                                break
                            end = raw.find(b'IEND\xaeB`\x82', begin)
                            if end < 0:
                                incomplete(f'Truncated embedded PNG: {name}'); break
                            end += 8
                            inspect_image(raw[begin:end], f'{name} [PNG at {begin}]')
                            offset, count = end, count + 1
                        if count == 100:
                            incomplete(f'Embedded image limit reached: {name}')
        except Exception as exc:
            incomplete(f'Archive scan incomplete: {type(exc).__name__}: {exc}')
        try:
            result['api_status'], findings = analyzer.analyze()
            result['api'] = [f.to_dict() for f in findings]
            permissions = set()
            # For multi-mod archives use the conservative intersection of grants.
            grants = []
            for path, raw_manifest in analyzer.files.items():
                try:
                    manifest = json.loads(raw_manifest)
                    if isinstance(manifest, dict) and isinstance(manifest.get('permissions', []), list):
                        grants.append({p for p in manifest.get('permissions', []) if isinstance(p, str)})
                except (ValueError, UnicodeError): pass
            if grants: permissions = set.intersection(*grants)
            checked = subprocess.run(['node', '--jitless', '--max-old-space-size=128', str(ROOT / 'sandbox-check.mjs')],
                input=json.dumps({'files': lua_files, 'permissions': sorted(permissions)}),
                capture_output=True, text=True, timeout=30, check=True)
            sandbox = json.loads(checked.stdout)
            for category, severity in [('errors', 'error'), ('warnings', 'warning')]:
                for f in sandbox[category]:
                    result['api'].append({'file_path': f['name'], 'line': f['line'], 'rule_id': 'SANDBOX', 'severity': severity,
                                          'message': f['message'], 'suggestion': 'Use the supported sandbox API and declared permissions.'})
            if result['api']: result['api_status'] = 'ISSUES'
        except Exception:
            incomplete('API analysis failed')
        result['exact_unique'], result['similar_unique'] = len(exact), len(similar)
        if any(a['kind'] == 'rom_signature' for a in result['assets']) or len(exact) >= self.policy['auto_quarantine_exact']:
            result['status'] = 'quarantined'
        elif not result['complete']:
            result['status'] = 'incomplete'
        elif result['assets'] or result['api']:
            result['status'] = 'review'
        result['priority'] = result['status'] == 'quarantined' or len(similar) >= self.policy['priority_similarity']
        result['elapsed_seconds'] = round(time.monotonic() - started, 2)
        return json.loads(redact(json.dumps(result)))
