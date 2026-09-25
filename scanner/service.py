"""Local review UI and trusted nightly controller, isolated from PR execution."""
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import html
import json
import os
from pathlib import Path
import secrets
import threading
import time
from urllib.parse import urlsplit, parse_qs
from zoneinfo import ZoneInfo

from catalog import REPO, remote_entries
from engine import Engine, redact
from jobs import scan_entry
from notify import deliver, payload, secret
from store import Store
from import_reports import import_reports

STATE = Path(os.environ.get('REVIEW_STATE', '/state'))
STATE.mkdir(parents=True, exist_ok=True)
STORE = Store(Path(os.environ.get('REVIEW_DATABASE', str(STATE / 'review.sqlite3'))))
LOCK = threading.Lock()
CSRF = secrets.token_urlsafe(32)
ENGINE = None
TZ = ZoneInfo(os.environ.get('TZ', 'America/New_York'))


def publish():
    """Publish only policy state, never assets or local paths, using an atomic Contents update."""
    import base64, requests
    if os.environ.get('PUBLISH_QUARANTINE') != '1': return
    token = secret('GH_TOKEN')
    if not token: raise ValueError('GitHub publishing credential missing')
    doc = STORE.quarantine_manifest()
    url = f'https://api.github.com/repos/{REPO}/contents/.health/moderation.json'
    headers = {'Authorization': f'Bearer {token}', 'Accept': 'application/vnd.github+json'}
    for attempt in range(3):
        response = requests.get(url, headers=headers, timeout=30)
        if response.status_code not in (200, 404): response.raise_for_status()
        before = response.json() if response.status_code == 200 else None
        if before:
            current = json.loads(base64.b64decode(before['content']))
            # Preserve decisions for entries not scanned by this installation yet.
            known = {r['key'] for r in STORE.latest()}
            doc['entries'].update({k: v for k, v in current.get('entries', {}).items() if k not in known})
            doc['approvals'].update({k: v for k, v in current.get('approvals', {}).items() if k not in known})
            if current == doc:
                STORE.set('publish_error', None); return
        content = base64.b64encode((json.dumps(doc, indent=2) + '\n').encode()).decode()
        request = {'message': 'Update mod moderation decisions', 'content': content, 'branch': 'main'}
        if before: request['sha'] = before['sha']
        saved = requests.put(url, headers=headers, json=request, timeout=30)
        if saved.status_code == 409: continue
        saved.raise_for_status()
        STORE.set('published_at', int(time.time())); STORE.set('publish_error', None); return
    raise ValueError('Concurrent moderation update; retry required')


def safe_publish():
    try: publish()
    except Exception as exc: STORE.set('publish_error', redact(f'{type(exc).__name__}: {exc}'))


def full_scan():
    global ENGINE
    if not LOCK.acquire(False): return
    try:
        STORE.set('running', True); STORE.set('last_error', None)
        ENGINE = ENGINE or Engine()
        entries = remote_entries(secret('GH_TOKEN'))
        STORE.set('progress', {'done': 0, 'total': len(entries)})
        for number, entry in enumerate(entries, 1):
            record = scan_entry(entry, ENGINE, secret('GH_TOKEN'), STATE / 'cache')
            scan_id = STORE.record(record)
            effective = STORE.effective(record)
            if effective.get('priority') and effective['status'] != 'approved':
                # A localhost link is intentionally not sent to the phone.
                review_url = os.environ.get('REVIEW_PUBLIC_URL') or f'https://github.com/{REPO}/actions'
                if os.environ.get('REVIEW_PUBLIC_URL'): review_url += f'/review/{scan_id}'
                key, body = payload(effective, review_url)
                body['text'] += ' Full evidence is on the local review dashboard at port 8849.'
                STORE.enqueue(key, body)
                deliver(STORE)
            STORE.set('progress', {'done': number, 'total': len(entries), 'entry': entry['key']})
            # Quarantine takes effect before waiting for the entire index scan.
            if effective['status'] == 'quarantined': safe_publish()
        safe_publish()
        STORE.set('last_scan', int(time.time()))
        STORE.set('scheduled_day', datetime.now(TZ).date().isoformat())
    except Exception as exc:
        STORE.set('last_error', redact(f'{type(exc).__name__}: {exc}'))
    finally:
        STORE.backup(STATE / 'backups' / 'review.sqlite3')
        STORE.set('running', False); LOCK.release()


def scheduler():
    STORE.set('running', False)
    last_import = 0
    while True:
        now = datetime.now(TZ)
        day = now.date().isoformat()
        last = STORE.setting('scheduled_day')
        if last != day and not LOCK.locked() and time.time() - STORE.setting('last_attempt', 0) >= 3600:
            # Startup catches missed midnight runs; at most one daily attempt.
            STORE.set('last_attempt', int(time.time()))
            threading.Thread(target=full_scan, daemon=True).start()
        if now.hour >= 8 and STORE.setting('digest_day') != day:
            records = [r for r in STORE.latest() if r['status'] in ('review', 'incomplete') and not r.get('priority')]
            fingerprint = sorted((r['key'], r.get('sha256'), r['status'], r.get('scanner')) for r in records)
            if records and STORE.setting('digest_fingerprint') != [list(x) for x in fingerprint]:
                STORE.enqueue('digest-' + day, {'id': 'mod-review-digest', 'threadId': 'mod-review', 'title': 'Mod review queue',
                    'text': f'{len(records)} mods need review or a successful rescan. Open the review dashboard on this machine at localhost:8849.',
                    'sound': 'subtle', 'isTimeSensitive': False,
                    'defaultAction': {'url': os.environ.get('REVIEW_PUBLIC_URL') or f'https://github.com/{REPO}/actions'}})
                STORE.set('digest_fingerprint', fingerprint)
            STORE.set('digest_day', day)
        deliver(STORE)
        if time.time() - last_import >= 300:
            try:
                import_reports(STORE, secret('GH_TOKEN'))
                STORE.set('import_error', None)
            except Exception:
                STORE.set('import_error', 'CI evidence sync unavailable; retrying in five minutes')
            last_import = time.time()
        if STORE.setting('publish_error'): safe_publish()
        time.sleep(60)


STYLE = '''body{font:16px system-ui;margin:32px auto;max-width:1200px;padding:0 24px;background:#101820;color:#e9eff4}a{color:#80caff}table{width:100%;border-collapse:collapse}td,th{text-align:left;padding:12px;border-bottom:1px solid #405060}button,input{font:inherit;padding:10px;margin:5px}button{cursor:pointer}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#172632;padding:18px}img{max-width:100%;image-rendering:pixelated}.quarantined{color:#ff8888}.review,.incomplete{color:#ffcf77}.clean,.approved{color:#84e8af}small{color:#b7c5d0}form{display:inline}'''


def esc(value): return html.escape(str(value), quote=True)


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *_): pass

    def send(self, status, body, mime='text/html; charset=utf-8'):
        raw = body.encode() if isinstance(body, str) else body
        self.send_response(status); self.send_header('Content-Type', mime)
        self.send_header('Content-Length', str(len(raw))); self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('Content-Security-Policy', "default-src 'none'; style-src 'unsafe-inline'; img-src data:; form-action 'self'; frame-ancestors 'none'; base-uri 'none'")
        self.end_headers(); self.wfile.write(raw)

    def valid_host(self):
        return self.headers.get('Host') in ('localhost:8849', '127.0.0.1:8849')

    def page(self, title, body):
        self.send(200, f'<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>{esc(title)}</title><style>{STYLE}</style></head><body><a href="/">Mod review</a><h1>{esc(title)}</h1>{body}</body></html>')

    def form(self, action, label, scan_id=''):
        note = '<input name="note" placeholder="Decision note" aria-label="Decision note" maxlength="2000">' if action in ('approve', 'quarantine') else ''
        return f'<form method="post" action="/{action}"><input type="hidden" name="csrf" value="{CSRF}"><input type="hidden" name="scan_id" value="{esc(scan_id)}">{note}<button>{esc(label)}</button></form>'

    def do_GET(self):
        if not self.valid_host(): return self.send(403, 'Invalid host')
        path = urlsplit(self.path).path
        if path == '/health':
            return self.send(200, json.dumps({'ok': True, 'running': STORE.setting('running', False), 'progress': STORE.setting('progress'),
                'last_scan': STORE.setting('last_scan'), 'last_error': STORE.setting('last_error'), 'publish_error': STORE.setting('publish_error'),
                'notification_error': STORE.setting('notification_error')}), 'application/json')
        if path.startswith('/review/'):
            try: record = STORE.get(int(path.split('/')[-1]))
            except ValueError: record = None
            if not record: return self.send(404, 'Scan not found')
            body = f"<p class='{esc(record['status'])}'>{esc(record['status'])}</p><p>{esc(record['key'])}</p>"
            body += '<p>Decisions apply only to this ZIP checksum. Incomplete scans cannot be approved.</p>'
            for action, label in [('approve', 'Approve this artifact'), ('quarantine', 'Quarantine this artifact'), ('reset', 'Reset decision')]:
                body += self.form(action, label, record['scan_id'])
            for preview in record.get('previews', []):
                body += f"<p>{esc(preview['path'])} → {esc(preview['reference'])}</p><img alt='Mod asset, reference, and difference' src='data:image/png;base64,{esc(preview['image'])}'>"
            if record.get('assets'):
                body += '<h2>Asset evidence</h2><table><tr><th>File</th><th>Match</th><th>Reference</th><th>Distance</th></tr>'
                for a in record['assets'][:1000]:
                    body += f"<tr><td>{esc(a.get('path', ''))}</td><td>{esc(a.get('kind', ''))}</td><td>{esc(a.get('reference', a.get('message', '')))}</td><td>{esc(a.get('distance', ''))}</td></tr>"
                body += '</table>'
            if record.get('api'):
                body += '<h2>Compatibility findings</h2><table><tr><th>Location</th><th>Rule</th><th>Finding and fix</th></tr>'
                for a in record['api'][:1000]:
                    body += f"<tr><td>{esc(a.get('file_path', ''))}:{esc(a.get('line', ''))}</td><td>{esc(a.get('rule_id', ''))} {esc(a.get('severity', ''))}</td><td>{esc(a.get('message', ''))}<br><small>{esc(a.get('suggestion', ''))}</small></td></tr>"
                body += '</table>'
            display = {k: v for k, v in record.items() if k != 'previews'}
            body += '<details><summary>Full machine readable report</summary><pre>' + esc(json.dumps(display, indent=2)) + '</pre></details>'
            return self.page(record['title'], body)
        if path != '/': return self.send(404, 'Not found')
        records = STORE.latest()
        query = parse_qs(urlsplit(self.path).query)
        search = query.get('q', [''])[0].lower()
        selected = query.get('status', [''])[0]
        total = len(records)
        records = [r for r in records if (not selected or r['status'] == selected) and (search in (r['title'] + r['key']).lower())]
        records.sort(key=lambda r: ({'quarantined': 0, 'review': 1, 'incomplete': 2}.get(r['status'], 3), -r.get('exact_unique', 0), -r.get('similar_unique', 0)))
        body = self.form('scan', 'Scan all mods now') + self.form('publish', 'Sync quarantine to GitHub')
        body += f"<p>Midnight scans · America/New_York · Morning digest after 08:00 · {total} entries checked</p>"
        body += f'<form method="get"><input name="q" aria-label="Search mods" placeholder="Search mods" value="{esc(search)}"><select name="status" aria-label="Status filter">'
        for status in ['', 'quarantined', 'review', 'incomplete', 'approved', 'clean']:
            body += f'<option value="{status}" {"selected" if status == selected else ""}>{status or "All statuses"}</option>'
        body += '</select><button>Filter</button></form>'
        body += '<p>Refresh this page to see progress. Quarantined listings are excluded from the published index after the next Pages deployment.</p>'
        for key in ['progress', 'last_error', 'publish_error', 'notification_error', 'import_error']:
            value = STORE.setting(key)
            if value: body += f'<p>{esc(key)}: {esc(value)}</p>'
        body += '<table><tr><th>Mod</th><th>Status</th><th>Exact assets</th><th>Similar assets</th><th>API findings</th></tr>'
        for r in records:
            body += f"<tr><td><a href='/review/{r['scan_id']}'>{esc(r['title'])}</a><br><small>{esc(r['key'])}</small></td><td class='{esc(r['status'])}'>{esc(r['status'])}</td><td>{r.get('exact_unique', 0)}</td><td>{r.get('similar_unique', 0)}</td><td>{len(r.get('api', []))}</td></tr>"
        body += '</table><details><summary>Recent scan history</summary><ul>'
        for r in STORE.recent(): body += f"<li><a href='/review/{r['scan_id']}'>{esc(r['key'])}</a> {esc(r['status'])} {esc(r['origin'])}</li>"
        self.page('Mod review queue', body + '</ul></details>')

    def do_POST(self):
        if not self.valid_host(): return self.send(403, 'Invalid host')
        origin = self.headers.get('Origin')
        if origin and origin not in ('http://localhost:8849', 'http://127.0.0.1:8849'):
            return self.send(403, 'Invalid origin')
        try:
            size = int(self.headers.get('Content-Length', 0))
            if size > 8192: raise ValueError('Request too large')
            data = parse_qs(self.rfile.read(size).decode())
            if not secrets.compare_digest(data.get('csrf', [''])[0], CSRF): return self.send(403, 'Invalid form token')
            action = self.path.strip('/')
            if action == 'scan': threading.Thread(target=full_scan, daemon=True).start()
            elif action == 'publish': threading.Thread(target=safe_publish, daemon=True).start()
            elif action in ('approve', 'quarantine', 'reset'):
                STORE.decide(int(data['scan_id'][0]), action, data.get('note', ['Local dashboard decision'])[0])
                threading.Thread(target=safe_publish, daemon=True).start()
            else: return self.send(404, 'Not found')
            self.send_response(303); self.send_header('Location', '/'); self.end_headers()
        except (ValueError, KeyError) as exc: self.send(400, esc(exc))


if __name__ == '__main__':
    threading.Thread(target=scheduler, daemon=True).start()
    ThreadingHTTPServer(('0.0.0.0', 8849), Handler).serve_forever()
