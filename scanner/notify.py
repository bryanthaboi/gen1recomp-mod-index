import hashlib
import json
import os
from pathlib import Path
import requests
from engine import redact


def secret(name):
    path = os.environ.get(name + '_FILE')
    return Path(path).read_text().strip() if path else os.environ.get(name, '')


def payload(record, review_url):
    key = hashlib.sha256(f"{record['key']}:{record.get('sha256')}:{record['status']}:{record.get('scanner')}".encode()).hexdigest()[:32]
    body = {'id': key, 'threadId': record['key'], 'title': f"{record['status'].title()}: {record['title']}",
            'text': f"{record.get('exact_unique', 0)} distinct exact assets; {record.get('similar_unique', 0)} similar assets; {len(record.get('api', []))} API findings.",
            'isTimeSensitive': bool(record.get('priority')), 'sound': 'problem' if record.get('priority') else 'subtle',
            'defaultAction': {'url': review_url}, 'actions': [{'name': 'Review evidence', 'url': review_url, 'keepNotification': True}]}
    url = ((record.get('release') or {}).get('zip') or {}).get('url')
    if url: body['actions'].append({'name': 'Open release', 'url': url})
    if record.get('previews'): body['imageData'] = record['previews'][0]['image']
    return key, json.loads(redact(json.dumps(body)))


def deliver(store):
    url = secret('PUSHCUT_WEBHOOK_URL')
    if not url: return
    for item in store.pending():
        try:
            response = requests.post(url, json=json.loads(item['body']), timeout=20, allow_redirects=False)
            success = 200 <= response.status_code < 300
            store.delivery(item['id'], success)
            if not success:
                store.set('notification_error', f"Pushcut HTTP {response.status_code}; delivery queued for retry")
                break
            store.set('notification_error', None)
        except requests.RequestException:
            store.delivery(item['id'], False)
            store.set('notification_error', 'Pushcut unavailable; delivery queued for retry')
            break
