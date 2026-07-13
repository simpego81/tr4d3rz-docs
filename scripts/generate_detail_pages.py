#!/usr/bin/env python3
"""
TR4D3RZ — Detail Page Generator (PMAP-08)

Reads docs/data/generated/roadmap.json and generates one static HTML file
per entity (milestone + task) in docs/details/roadmap/<id>.html.

Each page:
  - Embeds entity JSON for instant render (no extra fetch)
  - Embeds cross-links index (all entity IDs + names + detail_urls)
  - Uses shared/detail-renderer.js + shared/components.js for rendering
  - Has breadcrumb, back link, and static fallback table

Usage:
    python scripts/generate_detail_pages.py [--dry-run]
"""

import json
import os
import sys
import html as html_lib
from pathlib import Path
from datetime import datetime, timezone

REPO_ROOT  = Path(__file__).parent.parent
ROADMAP_JSON = REPO_ROOT / 'docs' / 'data' / 'generated' / 'roadmap.json'
OUT_DIR    = REPO_ROOT / 'docs' / 'details' / 'roadmap'
DRY_RUN    = '--dry-run' in sys.argv

# Relative path from docs/details/roadmap/ back to docs/
DEPTH = '../../'


def esc(s):
    return html_lib.escape(str(s) if s is not None else '', quote=True)


def load_roadmap():
    with open(ROADMAP_JSON, encoding='utf-8') as f:
        return json.load(f)


def build_cross_links(roadmap):
    """Build {id: {name, detail_url, status, health}} for cross-link resolution."""
    index = {}
    for entity in roadmap.get('milestones', []) + roadmap.get('tasks', []):
        d = entity.get('raw_data', {})
        index[entity['id']] = {
            'id':         entity['id'],
            'name':       entity.get('name', entity['id']),
            'kind':       entity.get('kind', 'entity'),
            'detail_url': d.get('detail_url', ''),
            'status':     d.get('status', 'UNKNOWN'),
            'health':     d.get('health', 'UNKNOWN'),
        }
    return index


def render_static_table(d):
    """Render a minimal HTML table for <noscript> fallback."""
    rows = []
    def row(label, value):
        rows.append(f'<tr><th scope="row">{esc(label)}</th><td>{esc(value)}</td></tr>')

    row('Status',   d.get('status', '—'))
    row('Health',   d.get('health', '—'))
    row('Freshness', d.get('freshness', '—'))
    row('Updated',  d.get('updated_at', '—'))

    owners = d.get('owners', [])
    if owners:
        row('Owners', ', '.join(f"{o.get('agent','?')} ({o.get('role','?')})" for o in owners))
    else:
        row('Owners', '—')

    deps = d.get('dependencies', [])
    row('Dependencies', ', '.join(deps) if deps else '—')

    blockers = d.get('blockers', [])
    if blockers:
        row('Blockers', '; '.join(b.get('description', '?') for b in blockers))
    else:
        row('Blockers', '—')

    summary = esc(d.get('summary', '—'))

    return f'''
<noscript>
  <div class="static-fallback" role="note">
    <h2>Static view (JavaScript disabled)</h2>
    <p>{summary}</p>
    <table class="fallback-table">
      <caption>Entity metadata</caption>
      <tbody>{''.join(rows)}</tbody>
    </table>
    <p class="mt-md"><a href="{DEPTH}maps/roadmap.html">← Back to Roadmap</a></p>
  </div>
</noscript>'''


def render_page(entity, cross_links):
    d   = entity.get('raw_data', {})
    eid = entity['id']
    name = entity.get('name', eid)
    kind = entity.get('kind', 'entity')

    entity_json   = json.dumps(entity,      ensure_ascii=False, separators=(',', ':'))
    crosslink_json = json.dumps(cross_links, ensure_ascii=False, separators=(',', ':'))

    # Breadcrumb / back path relative to docs/details/roadmap/
    map_href     = f'{DEPTH}index-new.html'
    roadmap_href = f'{DEPTH}maps/roadmap.html'

    static_table = render_static_table(d)

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{esc(name)} — TR4D3RZ Project Map</title>
  <meta name="description" content="{esc(d.get('summary', '')[:160])}">
  <link rel="stylesheet" href="{DEPTH}shared/design-tokens.css">
  <link rel="stylesheet" href="{DEPTH}shared/base.css">
</head>
<body>
  <a href="#main-content" class="skip-link">Skip to main content</a>

  <header class="header">
    <div class="container header-content">
      <p class="header-title"><a href="{map_href}" style="color:inherit;text-decoration:none">TR4D3RZ</a></p>
      <nav class="header-nav" role="navigation" aria-label="Main navigation">
        <a href="{map_href}">Project Map</a>
        <a href="{roadmap_href}">Roadmap</a>
      </nav>
    </div>
  </header>

  <main class="main" id="main-content">
    <div class="container">
      <div id="detail-root" aria-live="polite">
        <div class="loading" role="status"><span>Loading…</span></div>
      </div>
      {static_table}
    </div>
  </main>

  <footer class="footer">
    <div class="container">
      <p>TR4D3RZ Documentation &mdash; <a href="{DEPTH}maps/roadmap.html">Roadmap</a></p>
      <p class="text-xs mt-sm">Auto-generated from <code>state/roadmap.yaml</code></p>
    </div>
  </footer>

  <script type="application/json" id="entity-data">{entity_json}</script>
  <script type="application/json" id="cross-links">{crosslink_json}</script>
  <script src="{DEPTH}shared/data-loader.js"></script>
  <script src="{DEPTH}shared/components.js"></script>
  <script src="{DEPTH}shared/detail-renderer.js"></script>
  <script>
    (function () {{
      const entity     = JSON.parse(document.getElementById('entity-data').textContent);
      const crossLinks = JSON.parse(document.getElementById('cross-links').textContent);
      const root       = document.getElementById('detail-root');
      try {{
        DetailRenderer.render(root, entity, {{ allEntities: crossLinks }});
      }} catch (err) {{
        root.innerHTML = '<div class="error" role="alert"><div class="error-title">Render error</div><p>' +
          DataLoader.escapeHtml(err.message) + '</p></div>';
        console.error('[DetailRenderer]', err);
      }}
    }})();
  </script>
</body>
</html>
'''


def generate_all(roadmap):
    cross_links = build_cross_links(roadmap)
    entities = roadmap.get('milestones', []) + roadmap.get('tasks', [])

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    generated = []
    for entity in entities:
        eid      = entity['id']
        out_path = OUT_DIR / f'{eid}.html'
        html     = render_page(entity, cross_links)

        if DRY_RUN:
            print(f'  [dry-run] would write {out_path.relative_to(REPO_ROOT)}')
        else:
            out_path.write_text(html, encoding='utf-8')
            print(f'  [OK] {out_path.relative_to(REPO_ROOT)}')
        generated.append(str(out_path.relative_to(REPO_ROOT)))

    return generated


def main():
    print(f'Loading {ROADMAP_JSON.relative_to(REPO_ROOT)}…')
    roadmap = load_roadmap()

    milestones = roadmap.get('milestones', [])
    tasks      = roadmap.get('tasks',      [])
    total      = len(milestones) + len(tasks)
    print(f'  {len(milestones)} milestones, {len(tasks)} tasks -> {total} pages')

    if DRY_RUN:
        print('Dry-run mode — no files written')

    generated = generate_all(roadmap)

    ts = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    print(f'\n[OK] Generated {len(generated)} detail pages in {OUT_DIR.relative_to(REPO_ROOT)}/')
    print(f'     Timestamp: {ts}')


if __name__ == '__main__':
    main()
