"""Import bounded workflow reports as history only, never as moderation authority."""
import io
import json
import re
import time
import zipfile
from catalog import REPO
from engine import fetch, json_get, redact


def import_reports(store, token):
    artifacts = json_get(f'https://api.github.com/repos/{REPO}/actions/artifacts?per_page=30', token)
    seen = set(store.setting('imported_artifacts', []))
    for artifact in reversed(artifacts.get('artifacts', [])):
        if artifact['id'] in seen or artifact['name'] != 'mod-scan-report' or artifact.get('expired'):
            continue
        if artifact['size_in_bytes'] > 32 * 1024 * 1024:
            continue
        blob = fetch(artifact['archive_download_url'], 32 * 1024 * 1024, token)
        with zipfile.ZipFile(io.BytesIO(blob)) as z:
            info = next((i for i in z.infolist() if i.filename == 'scan-report.json'), None)
            if info is None or info.file_size > 64 * 1024 * 1024:
                continue
            report = json.loads(z.read(info))
        entries = report.get('entries')
        if not isinstance(entries, list) or len(entries) > 2000: continue
        for record in entries:
            if not isinstance(record, dict) or not re.fullmatch(r'(mods|carts)/[^/]{1,200}', str(record.get('key', ''))): continue
            if record.get('status') not in ('clean', 'review', 'incomplete', 'quarantined', 'approved'): continue
            if not re.fullmatch(r'[a-f0-9]{64}|', str(record.get('sha256', ''))): continue
            if not isinstance(record.get('title'), str): continue
            if any(not isinstance(record.get(k, []), list) for k in ('assets', 'api', 'previews', 'errors')): continue
            if any(not isinstance(a, dict) for k in ('assets', 'api', 'previews') for a in record.get(k, [])): continue
            record['previews'] = [p for p in record.get('previews', [])[:12] if all(isinstance(p.get(k), str) for k in ('path', 'reference', 'image')) and len(p['image']) < 2000000 and re.fullmatch(r'[A-Za-z0-9+/=]+', p['image'])]
            record['checked_at'] = int(time.time())
            # Reports may originate from PR-controlled jobs. Store as evidence only.
            record['source_run'] = f"https://github.com/{REPO}/actions/runs/{artifact.get('workflow_run', {}).get('id', '')}"
            store.record(json.loads(redact(json.dumps(record))), origin='ci untrusted evidence')
        seen.add(artifact['id'])
    store.set('imported_artifacts', sorted(seen)[-2000:])
