# Architecture Documentation Generation

This folder contains auto-generated ArchiMate documentation for TR4D3RZ.

## Quick Start

**Regenerate all documentation:**
```powershell
cd c:\projects\seq\tr4
powershell.exe -ExecutionPolicy Bypass -NoProfile -File .\generate_docs.ps1
```

This single command will:
1. ✓ Regenerate all `*.html` device pages
2. ✓ Update `archimate_data.json` for holistic view
3. ✓ Synchronize holistic view with PUML changes

## File Types

### Auto-Generated (DO NOT EDIT MANUALLY)
- `*.html` — Per-device ArchiMate views (except `holistic_view.html`)
- `archimate_data.json` — Aggregated data feed for holistic view

### Manual / Template Files
- `holistic_view.html` — D3.js concentric visualization (loads `archimate_data.json`)
- `index.html` — Homepage with device grid

## Making Changes

1. Edit `device_*.puml` files in repository root
2. Run `generate_docs.ps1`
3. Commit both PUML and generated HTML/JSON files

**Never edit HTML files directly** — changes will be overwritten on next generation.

## Viewing Locally

Open in browser:
- `docs/index.html` — Device grid homepage
- `docs/<device>.html` — Per-device view
- `docs/holistic_view.html` — Concentric holistic view

## Publishing

Commit changes to `main` branch:
```bash
git add device_*.puml docs/*.html docs/archimate_data.json
git commit -m "docs(arch): update architecture diagrams"
git push
```

GitHub Pages automatically deploys: https://simpego81.github.io/tr4d3rz-docs/

---

For detailed workflow documentation, see: `../ARCHITECTURE_WORKFLOW.md`
