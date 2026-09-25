"""Resolve the same artifacts as the index and expand pinned cart dependencies."""
import json
from pathlib import Path
import re
from urllib.parse import quote
from engine import json_get

REPO = 'bryanthaboi/gen1recomp-mod-index'


def release_for(meta, token='', extension='.zip'):
    if not meta.get('github') or meta.get('automatic_version_check') is False:
        if meta.get('downloadURL'):
            return {'version': meta.get('version'), 'zip': {'url': meta['downloadURL']}}
        return None
    repo = meta['github']
    if not re.fullmatch(r'[\w.-]+/[\w.-]+', repo):
        raise ValueError('Invalid GitHub repository')
    releases = json_get(f'https://api.github.com/repos/{repo}/releases?per_page=30', token)
    pinned = meta.get('fixed_release_tag')
    candidates = []
    for release in releases:
        if release.get('draft') or (pinned and release['tag_name'] != pinned):
            continue
        match = re.match(r'\d+\.\d+\.\d+', release['tag_name'].lstrip('vV'))
        if not match:
            continue
        version = match[0]
        assets = [a for a in release.get('assets', []) if a['name'].lower().endswith(extension)]
        exact = f"{meta['id']}-{version}{extension}".lower()
        assets.sort(key=lambda a: (a['name'].lower() != exact, not a['name'].lower().startswith(meta['id'].lower())))
        if assets:
            asset = assets[0]
            candidates.append({'version': version, 'tag': release['tag_name'], 'prerelease': release.get('prerelease', False),
                               'zip': {'url': asset['browser_download_url'], 'name': asset['name']}})
    return next((r for r in candidates if not r['prerelease']), candidates[0] if candidates else None)


def local_entries(root, changed=None):
    entries = []
    for kind in ('mods', 'carts'):
        for path in sorted((Path(root) / kind).glob('*/meta.json')):
            folder = f'{kind}/{path.parent.name}'
            if changed is not None and folder not in changed:
                continue
            entries.append({'key': folder, 'kind': kind, 'meta': json.loads(path.read_text())})
    return entries


def remote_entries(token=''):
    tree = json_get(f'https://api.github.com/repos/{REPO}/git/trees/main?recursive=1', token)
    if tree.get('truncated'):
        raise ValueError('Repository tree is truncated')
    entries = []
    for row in tree['tree']:
        if re.fullmatch(r'(mods|carts)/[^/]+/meta.json', row['path']):
            path = row['path']
            meta = json_get(f'https://raw.githubusercontent.com/{REPO}/main/{quote(path)}')
            entries.append({'key': path.rsplit('/', 1)[0], 'kind': path.split('/')[0], 'meta': meta})
    if not entries:
        raise ValueError('No entries found in repository')
    return entries


def pin_release(pin, token=''):
    if pin['source'] == 'github':
        meta = {'github': pin['repo'], 'id': pin['id']}
        releases = json_get(f"https://api.github.com/repos/{pin['repo']}/releases?per_page=100", token)
        release = next((r for r in releases if r['tag_name'].lstrip('vV') == pin['version']), None)
        if not release:
            raise ValueError('Pinned release not found')
        assets = [a for a in release.get('assets', []) if a['name'].lower().endswith('.zip')]
        exact = f"{pin['id']}-{pin['version']}.zip".lower()
        assets.sort(key=lambda a: (a['name'].lower() != exact, not a['name'].lower().startswith(pin['id'].lower())))
        if not assets:
            raise ValueError('Pinned release has no ZIP')
        return assets[0]['browser_download_url'], 'sha256', pin['sha256']
    if pin['source'] == 'gamebanana':
        doc = json_get(f"https://gamebanana.com/apiv11/Mod/{int(pin['mod'])}/ProfilePage")
        file = next((f for f in doc.get('_aFiles', []) if str(f['_idRow']) == str(pin['file'])), None)
        if not file:
            raise ValueError('Pinned GameBanana file missing')
        return file['_sDownloadUrl'], 'md5', pin['md5']
    raise ValueError('Unsupported cart pin source')
