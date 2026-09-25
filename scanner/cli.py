import argparse
import json
import os
from pathlib import Path
import subprocess
from catalog import local_entries
from engine import Engine, build_references, redact, json_get
from jobs import scan_entry


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', default='.')
    parser.add_argument('--base')
    parser.add_argument('--output', default='scan-report.json')
    parser.add_argument('--gate-index', help='Scan exactly these resolved artifacts and remove unverified or quarantined releases from this feed')
    parser.add_argument('--cache')
    parser.add_argument('--build-references', nargs=2, metavar=('IMAGES', 'OUTPUT'))
    args = parser.parse_args()
    if args.build_references:
        print('Reference entries:', build_references(*args.build_references)); return 0
    engine = Engine()
    # Only maintainer state on main can approve an artifact, never PR-supplied JSON.
    import requests
    try:
        moderation = json_get('https://raw.githubusercontent.com/bryanthaboi/gen1recomp-mod-index/main/.health/moderation.json')
    except requests.HTTPError as exc:
        if exc.response.status_code != 404: raise
        moderation = {'entries': {}, 'approvals': {}}
    changed = None
    if args.base:
        names = subprocess.check_output(['git', 'diff', '--name-only', '-z', f'{args.base}...HEAD'], cwd=args.root).decode().split('\0')
        changed = {'/'.join(n.split('/')[:2]) for n in names if n.startswith(('mods/', 'carts/'))}
    records = []
    entries = local_entries(args.root, changed)
    if args.gate_index:
        feed = json.loads(Path(args.gate_index).read_text())
        entries = [{'key': f"{kind}/{meta['folder']}", 'kind': kind, 'meta': meta, 'resolved_release': meta.get('latest')}
                   for kind in ('mods', 'carts') for meta in feed.get(kind, [])]
    for entry in entries:
        record = scan_entry(entry, engine, os.environ.get('GITHUB_TOKEN', ''), args.cache)
        approved = moderation.get('approvals', {}).get(entry['key'], {}).get('sha256')
        if approved and approved == record.get('sha256') and record.get('complete'):
            record['status'] = 'approved'
        held = moderation.get('entries', {}).get(entry['key'])
        if held and held.get('sha256') == record.get('sha256'):
            record['status'] = 'quarantined'
        records.append(record)
        Path(args.output).write_text(json.dumps({'version': 1, 'entries': records}))
        print(redact(f"{entry['key']}: {record['status']} exact={record.get('exact_unique', 0)} similar={record.get('similar_unique', 0)}"))
    Path(args.output).write_text(json.dumps({'version': 1, 'entries': records}))
    if args.gate_index:
        denied = {r['key'] for r in records if r['status'] in ('quarantined', 'incomplete') or any(f['severity'] == 'error' for f in r.get('api', []))}
        for kind in ('mods', 'carts'):
            feed[kind] = [m for m in feed.get(kind, []) if f"{kind}/{m['folder']}" not in denied]
        feed['count'], feed['cart_count'] = len(feed['mods']), len(feed['carts'])
        # A widespread scan outage must not deploy an almost-empty catalog.
        if records and sum(r['status'] == 'incomplete' for r in records) > max(5, len(records) * .25):
            print('Publication stopped because too many scans were incomplete')
            return 1
        Path(args.gate_index).write_text(json.dumps(feed, indent=2) + '\n')
    summary = ['### Mod asset and compatibility scan', '', f'{len(records)} releases checked.', '']
    for r in records:
        summary.append(f"- {r['key'].replace('`', '')}: **{r['status']}**, {r.get('exact_unique', 0)} distinct exact matches, {r.get('similar_unique', 0)} similarity matches, {len(r.get('api', []))} API findings")
    if os.environ.get('GITHUB_STEP_SUMMARY'):
        with open(os.environ['GITHUB_STEP_SUMMARY'], 'a') as f: f.write(redact('\n'.join(summary)))
    return 0 if args.gate_index else int(any(r['status'] in ('quarantined', 'incomplete') or any(f['severity'] == 'error' for f in r.get('api', [])) for r in records))


if __name__ == '__main__':
    raise SystemExit(main())
