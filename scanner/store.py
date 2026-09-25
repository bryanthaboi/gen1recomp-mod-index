"""SQLite history, artifact-specific decisions, and durable notification outbox."""
import json
from contextlib import contextmanager
from pathlib import Path
import sqlite3
import time


class Store:
    def __init__(self, path):
        self.path = str(path)
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with self.connect() as db:
            db.executescript('''
                PRAGMA journal_mode=WAL;
                CREATE TABLE IF NOT EXISTS scans(id INTEGER PRIMARY KEY, entry TEXT, sha TEXT, checked INTEGER, report TEXT, origin TEXT);
                CREATE TABLE IF NOT EXISTS decisions(entry TEXT, sha TEXT, action TEXT, note TEXT, changed INTEGER, PRIMARY KEY(entry,sha));
                CREATE TABLE IF NOT EXISTS outbox(id TEXT PRIMARY KEY, body TEXT, sent INTEGER DEFAULT 0, attempts INTEGER DEFAULT 0);
                CREATE TABLE IF NOT EXISTS settings(key TEXT PRIMARY KEY, value TEXT);
                CREATE TABLE IF NOT EXISTS decision_events(id INTEGER PRIMARY KEY, entry TEXT, sha TEXT, action TEXT, note TEXT, changed INTEGER);
                CREATE INDEX IF NOT EXISTS scans_entry ON scans(entry, id DESC);
                CREATE TABLE IF NOT EXISTS quarantine_history(entry TEXT PRIMARY KEY, sha TEXT);
            ''')
            # Preserve historical quarantines when upgrading an existing database.
            for row in db.execute("SELECT entry,sha,report FROM scans WHERE origin='nightly'").fetchall():
                if json.loads(row['report']).get('status') == 'quarantined':
                    db.execute('INSERT OR IGNORE INTO quarantine_history VALUES (?,?)', (row['entry'], row['sha']))
            db.execute("INSERT OR IGNORE INTO quarantine_history SELECT entry,sha FROM decisions WHERE action='quarantine'")
            db.execute("INSERT OR IGNORE INTO quarantine_history SELECT entry,sha FROM decision_events WHERE action='quarantine'")

    @contextmanager
    def connect(self):
        db = sqlite3.connect(self.path, timeout=30)
        db.row_factory = sqlite3.Row
        try:
            with db: yield db
        finally:
            db.close()

    def backup(self, path):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with self.connect() as source:
            target = sqlite3.connect(path)
            try: source.backup(target)
            finally: target.close()

    def setting(self, key, default=None):
        with self.connect() as db:
            row = db.execute('SELECT value FROM settings WHERE key=?', (key,)).fetchone()
            return json.loads(row[0]) if row else default

    def set(self, key, value):
        with self.connect() as db:
            db.execute('INSERT OR REPLACE INTO settings VALUES (?,?)', (key, json.dumps(value)))

    def record(self, record, origin='nightly'):
        with self.connect() as db:
            if origin == 'nightly' and record['status'] == 'quarantined':
                db.execute('INSERT OR IGNORE INTO quarantine_history VALUES (?,?)', (record['key'], record.get('sha256', '')))
            cursor = db.execute('INSERT INTO scans(entry,sha,checked,report,origin) VALUES(?,?,?,?,?)',
                                (record['key'], record.get('sha256', ''), record['checked_at'], json.dumps(record), origin))
            return cursor.lastrowid

    def effective(self, record):
        with self.connect() as db:
            row = db.execute('SELECT * FROM decisions WHERE entry=? AND sha=?', (record['key'], record.get('sha256', ''))).fetchone()
            held = db.execute('SELECT sha FROM quarantine_history WHERE entry=?', (record['key'],)).fetchone()
        if held:
            record = {**record, 'scan_status': record['status'], 'priority': True,
                      'status': 'quarantined' if held['sha'] == record.get('sha256') else 'updated_recheck'}
        if row:
            record = {**record, 'decision': dict(row)}
            if row['action'] == 'approve' and record.get('complete'):
                record['status'] = 'approved'
            elif row['action'] == 'quarantine':
                record['status'] = 'quarantined'
        return record

    def latest(self):
        with self.connect() as db:
            rows = db.execute("SELECT * FROM scans WHERE id IN (SELECT MAX(id) FROM scans WHERE origin='nightly' GROUP BY entry)").fetchall()
        return [self.effective({**json.loads(r['report']), 'scan_id': r['id']}) for r in rows]

    def recent(self):
        with self.connect() as db:
            rows = db.execute('SELECT * FROM scans ORDER BY id DESC LIMIT 300').fetchall()
        return [self.effective({**json.loads(r['report']), 'scan_id': r['id'], 'origin': r['origin']}) for r in rows]

    def get(self, scan_id):
        with self.connect() as db:
            row = db.execute('SELECT * FROM scans WHERE id=?', (scan_id,)).fetchone()
        return self.effective({**json.loads(row['report']), 'scan_id': row['id']}) if row else None

    def decide(self, scan_id, action, note):
        record = self.get(scan_id)
        if not record or action not in ('approve', 'quarantine', 'reset'):
            raise ValueError('Decision requires a scanned artifact')
        if action == 'approve' and (not record.get('complete') or not record.get('sha256')):
            raise ValueError('Incomplete scans cannot be approved; rescan first')
        with self.connect() as db:
            db.execute('INSERT INTO decision_events(entry,sha,action,note,changed) VALUES(?,?,?,?,?)',
                       (record['key'], record['sha256'], action, note[:2000], int(time.time())))
            if action == 'reset':
                db.execute('DELETE FROM decisions WHERE entry=? AND sha=?', (record['key'], record['sha256']))
            else:
                db.execute('INSERT OR REPLACE INTO decisions VALUES(?,?,?,?,?)',
                           (record['key'], record['sha256'], action, note[:2000], int(time.time())))
                if action == 'quarantine':
                    db.execute('INSERT OR IGNORE INTO quarantine_history VALUES (?,?)', (record['key'], record['sha256']))

    def quarantine_manifest(self):
        entries = {}
        approvals = {}
        for r in self.latest():
            if r['status'] == 'approved':
                approvals[r['key']] = {'sha256': r['sha256']}
            if r['status'] in ('quarantined', 'updated_recheck'):
                entries[r['key']] = {'sha256': r['sha256'], 'version': (r.get('release') or {}).get('version'),
                                     'reason': 'Previously quarantined entry requires explicit approval of this artifact',
                                     'checked_at': r['checked_at']}
            elif r['status'] == 'incomplete':
                # An outage must never erase a previous quarantine.
                with self.connect() as db:
                    older = db.execute("SELECT report FROM scans WHERE entry=? AND origin='nightly' ORDER BY id DESC", (r['key'],)).fetchall()
                for row in older:
                    prior = self.effective(json.loads(row[0]))
                    if prior['status'] == 'incomplete': continue
                    if prior['status'] == 'quarantined':
                        entries[r['key']] = {'sha256': prior['sha256'], 'reason': 'Previous quarantine retained while latest scan is incomplete', 'checked_at': prior['checked_at']}
                    elif prior['status'] == 'approved':
                        approvals[r['key']] = {'sha256': prior['sha256']}
                    break
        with self.connect() as db:
            watchlist = {r['entry']: {'sha256': r['sha']} for r in db.execute('SELECT * FROM quarantine_history')}
        # Scan timestamps belong in local history, not policy: unchanged decisions
        # must not create a commit and deployment for every nightly rescan.
        for entry in entries.values(): entry.pop('checked_at', None)
        return {'version': 1, 'entries': entries, 'approvals': approvals, 'watchlist': watchlist}

    def enqueue(self, key, payload):
        with self.connect() as db:
            db.execute('INSERT OR IGNORE INTO outbox(id,body) VALUES(?,?)', (key, json.dumps(payload)))

    def pending(self):
        with self.connect() as db:
            return [dict(r) for r in db.execute('SELECT * FROM outbox WHERE sent=0 ORDER BY rowid LIMIT 20')]

    def delivery(self, key, success):
        with self.connect() as db:
            db.execute('UPDATE outbox SET attempts=attempts+1, sent=? WHERE id=?', (int(success), key))
