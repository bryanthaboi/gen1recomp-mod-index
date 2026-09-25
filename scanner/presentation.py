"""Escaped display helpers for scan metadata; no file contents are executed."""
from html import escape


def esc(value):
    return escape(str(value), quote=True)


def size(value):
    if value is None: return 'Not measured'
    value = max(0, int(value))
    for unit, divisor in [('GiB', 1024 ** 3), ('MiB', 1024 ** 2), ('KiB', 1024)]:
        if value >= divisor: return f'{value / divisor:,.2f} {unit}'
    return f'{value:,} B'


def card(label, value, detail=''):
    return f"<div class='stat'><small>{esc(label)}</small><strong>{esc(value)}</strong><span>{esc(detail)}</span></div>"


def summary(record):
    download = record.get('download', {})
    main_size = download.get('download_bytes', record.get('archive_bytes'))
    source = download.get('size_source', 'measured' if main_size is not None else 'rescan to measure')
    if source == 'at least': source = 'minimum received; total unknown'
    release = record.get('release') or {}
    artifact = release.get('zip') or {}
    body = "<section class='summary'><div class='eyebrow'>RELEASE OVERVIEW</div>"
    body += f"<p class='filename'>{esc(artifact.get('name') or 'Release artifact')} <span class='badge'>{esc(release.get('version') or 'Unknown version')}</span></p><div class='stats'>"
    detail = f"{main_size:,} bytes · {source}" if isinstance(main_size, int) else source
    body += card('Download size', size(main_size), detail)
    manifests = [f for f in record.get('file_stats', []) if f['path'] == 'manifest.json']
    if manifests: body += card('Main manifest', size(manifests[0]['bytes']), f"{manifests[0]['bytes']:,} bytes")
    body += card('Unpacked size', size(record.get('unpacked_bytes')), 'ZIP directory metadata')
    total = record.get('total_files')
    body += card('Files', f'{total:,}' if total is not None else 'Not inventoried', f"{record.get('files', 0):,} visited · {record.get('images', 0):,} images inspected")
    body += card('Asset matches', f"{record.get('exact_unique', 0):,} exact", f"{record.get('similar_unique', 0):,} similar · distinct reference assets")
    body += card('Compatibility', f"{len(record.get('api', [])):,} findings", f"Scan time {record.get('elapsed_seconds', '—')} seconds")
    body += "</div>"
    if download.get('download_limit_bytes'):
        body += f"<p class='muted'>Download limit {size(download['download_limit_bytes'])} · Unpacked limit 512 MiB · Per file limit 32 MiB · Per source limit 16 MiB</p>"
    if record.get('errors'):
        body += "<div class='issues'><strong>Scan limitations</strong><ul>" + ''.join(f'<li>{esc(e)}</li>' for e in record['errors'][:3]) + '</ul>'
        if len(record['errors']) > 3:
            body += f"<details><summary>{len(record['errors']) - 3} more recorded limitations</summary><ul>" + ''.join(f'<li>{esc(e)}</li>' for e in record['errors'][3:]) + '</ul></details>'
        body += '</div>'
    files = record.get('file_stats', [])
    if files:
        body += '<h2>Largest files and manifests</h2><div class="table-scroll"><table><tr><th>File</th><th>Unpacked</th><th>Compressed</th><th>Scan limit</th></tr>'
        for f in files:
            flag = 'Exceeds file limit' if f.get('over_member_limit') else 'Exceeds source limit' if f.get('over_source_limit') else 'Within per file limits'
            body += f"<tr><td class='file-path'>{esc(f['path'])}</td><td title='{int(f['bytes']):,} bytes'>{size(f['bytes'])}<small class='byte-count'>{int(f['bytes']):,} bytes</small></td><td>{size(f['compressed_bytes'])}</td><td>{esc(flag)}</td></tr>"
        body += '</table></div>'
    types = record.get('file_types', {})
    if types:
        body += '<details><summary>File types</summary><table><tr><th>Type</th><th>Files</th><th>Unpacked size</th></tr>'
        for ext, info in sorted(types.items(), key=lambda item: item[1]['bytes'], reverse=True):
            body += f"<tr><td>{esc(ext)}</td><td>{info['count']:,}</td><td>{size(info['bytes'])}</td></tr>"
        body += '</table></details>'
    return body + '</section>'


def progress_panel(progress, running):
    if not progress: return ''
    total = max(0, int(progress.get('total', 0)))
    done = min(total, max(0, int(progress.get('done', 0))))
    percent = round(done / total * 100) if total else 0
    title = 'Audit in progress' if running else 'Latest audit'
    entry = progress.get('entry', '')
    return f"<section class='progress-panel'><div class='progress-heading'><strong>{title}</strong><span>{done:,} / {total:,} entries · {percent}%</span></div><progress max='{max(total, 1)}' value='{done}' aria-label='Audit progress'></progress><p class='muted'>{esc(entry)}</p></section>"
