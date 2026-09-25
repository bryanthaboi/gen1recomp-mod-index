import hashlib
import errno
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
from catalog import release_for, pin_release
from engine import fetch, redact


def scan_process(data, engine, cache=None):
    """Run bounded scanning in a child; parser failures cannot kill the service."""
    sha = hashlib.sha256(data).hexdigest()
    cached = Path(cache) / f'{sha}-{engine.revision}.json' if cache else None
    if cached and cached.is_file():
        result = json.loads(cached.read_text())
        if result['complete']:
            return result
    with tempfile.TemporaryDirectory(prefix='scan-') as directory:
        archive = Path(directory) / 'release.zip'
        output = Path(directory) / 'result.json'
        archive.write_bytes(data)
        env = {k: v for k, v in os.environ.items() if k in {'PATH', 'LANG', 'REFERENCE_IMAGES', 'PYTHONPATH'}}
        completed = subprocess.run([sys.executable, str(Path(__file__).with_name('worker.py')), str(archive), str(output)],
                                   env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                                   timeout=engine.policy['max_seconds'] + 30)
        if completed.returncode or not output.is_file():
            raise ValueError('Scan worker failed or exceeded resource limits')
        result = json.loads(output.read_text())
        if cached and result['complete']:
            try:
                cached.parent.mkdir(parents=True, exist_ok=True)
                cached.write_text(json.dumps(result))
            except OSError as exc:
                # Read-only Docker mounts raise EROFS, not PermissionError.
                if exc.errno not in (errno.EROFS, errno.EACCES, errno.EPERM): raise
        return result


def scan_entry(entry, engine, token='', cache=None):
    record = {'key': entry['key'], 'title': entry['meta'].get('title', entry['key']), 'checked_at': int(time.time()), 'release': None}
    try:
        release = entry['resolved_release'] if 'resolved_release' in entry else release_for(entry['meta'], token, '.g1rcart' if entry['kind'] == 'carts' else '.zip')
        record['release'] = release
        if not release:
            raise ValueError('No installable release')
        record['download'] = {}
        data = fetch(release['zip']['url'], stats=record['download'])
        if entry['kind'] == 'carts':
            import base64, io, zipfile
            from cart import parse_bundle
            bundle = parse_bundle(data)
            cart = bundle['cart']
            if cart.get('id') != entry['meta'].get('id'): raise ValueError('Cart identity does not match the listing')
            packed = io.BytesIO()
            with zipfile.ZipFile(packed, 'w') as z:
                z.writestr('cart.json', json.dumps(cart))
                if bundle.get('labelArt'):
                    label = bundle['labelArt']
                    if label.get('encoding') != 'base64': raise ValueError('Unsupported label encoding')
                    image = base64.b64decode(label['data'], validate=True)
                    if len(image) != label['bytes'] or len(image) > 1024 * 1024: raise ValueError('Invalid cart label size')
                    z.writestr('label.png', image)
            record.update(scan_process(packed.getvalue(), engine, cache))
            record['sha256'] = hashlib.sha256(data).hexdigest()
            dependencies = []
            pins = cart.get('mods', [])
            if not isinstance(pins, list) or not 1 <= len(pins) <= 64: raise ValueError('Invalid cart pin list')
            for pin in pins:
                url, algorithm, expected = pin_release(pin, token)
                pinned = fetch(url)
                if hashlib.new(algorithm, pinned).hexdigest().lower() != expected.lower():
                    raise ValueError(f"Cart dependency checksum mismatch: {pin['id']}")
                scanned = scan_process(pinned, engine, cache)
                dependencies.append({'id': pin['id'], **scanned})
            record['dependencies'] = dependencies
            if any(d['status'] == 'quarantined' for d in dependencies):
                record['status'] = 'quarantined'
            elif any(not d['complete'] for d in dependencies):
                record['complete'] = False
                if record['status'] != 'quarantined': record['status'] = 'incomplete'
            elif any(d['status'] == 'review' for d in dependencies) and record['status'] == 'clean':
                record['status'] = 'review'
            record['priority'] = record['status'] == 'quarantined' or any(d['priority'] for d in dependencies)
        else:
            record.update(scan_process(data, engine, cache))
    except Exception as exc:
        record.setdefault('errors', []).append(redact(f'{type(exc).__name__}: {exc}'))
        record['complete'] = False
        if record.get('status') != 'quarantined': record['status'] = 'incomplete'
        record.setdefault('sha256', '')
        record.setdefault('scanner', engine.revision)
        if 'limit' in str(exc) and 'byte' in str(exc): record['priority'] = True
    return json.loads(redact(json.dumps(record)))
