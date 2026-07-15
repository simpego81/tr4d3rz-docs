# TR4D3RZ — DEMO REGISTRY

This registry tracks all functional demos, their purpose, and health status.

---

## Demo Registry

| ID | Title | Purpose | Status | Location |
|---|---|---|---|---|
| DEMO-001 | MVP Browser Demo | Validate M1 Architecture Simulation | ✅ HEALTHY | `tr4d3rz-docs/specs/mvp-browser-demo/` |
| DEMO-002 | Enhanced MVP Demo | Real Rust Component Integration | ✅ READY | `tr4d3rz-docs/demos/enhanced-mvp/` |

---

## Demo Details

### DEMO-001: MVP Browser Demo

- **Goal**: Full-stack simulation of M1 backbone (Scraper, Evolution, ESP, Logger).
- **Technology**: Node.js, Aedes MQTT, Browser UI.
- **Scenario**:
    1. Start Backend.
    2. Open UI.
    3. Observe simulated message flows between 5 nodes.
- **Observability**: Real-time event log, node status map, payload inspector.
- **Access**: `npm run demo` (in target dir).

---

## Demo Details

### DEMO-002: Enhanced MVP Demo

- **Goal**: Demonstrate real tr4d3rz-core component integration and M1 progress
- **Technology**: Node.js, Rust CLI bridge, tr4d3rz-core
- **Scenario**:
    1. Start server (`npm start`)
    2. Open http://localhost:3100
    3. Explore component status, M1 progress, and Rust data structures
- **Observability**: Component metrics, test status, CBOR size comparison, interactive data explorers
- **Access**: `cd tr4d3rz-docs/demos/enhanced-mvp && npm start`
- **Key Features**:
    - Real tr4d3rz-core types (not mocked)
    - Actual CBOR serialization
    - M1 task progress tracking
    - Interactive GenomeCapsule/FitnessResult/OHLCV explorers

---

### DEMO-003-PMAP: Project Map — GitHub Pages Progressive Project Map

- **Goal**: Dimostrare navigazione stakeholder, drill-down tecnico, aggiornamento SSOT, e failure injection controllata.
- **Technology**: Static HTML + D3.js, Python pipeline, GitHub Pages.
- **Status**: ✅ READY (scenari CLI verificati; scenari browser pending validazione umana)
- **Location**: `tr4d3rz-docs/docs/` (GitHub Pages) + `artifacts/features/FEATURE-DOCS-PROJECT-MAP/demo_script.md`
- **Feature**: FEATURE-DOCS-PROJECT-MAP (PMAP-18)
- **Scenari**:
    1. D-PMAP-01: Navigazione stakeholder mobile (390px) — homepage con metrics e 4 card
    2. D-PMAP-02: Drill-down tecnico — 4 mappe interattive + detail pages
    3. D-PMAP-03: Aggiornamento SSOT — modifica roadmap.yaml → rigenera → manifest aggiornato
    4. D-PMAP-04: Roadmap senza date — milestone non pianificate in corsia esplicita
    5. D-PMAP-05: Snapshot assente → MAP-E003 + badge STALE (CLI riproducibile)
    6. D-PMAP-06: Schema invalido → MAP-E001, publish bloccato (CLI riproducibile)
    7. D-PMAP-07: Generazione parziale → MAP-E007, no output parziale (CLI riproducibile)
    8. D-PMAP-08: Navigazione legacy — device-matrix.html e holistic_view.html accessibili
- **Observability**: `docs/data/generated/build-manifest.json` — errors, warnings, freshness, durations
- **Access**: `python scripts/build_project_map.py --verbose` + aprire `docs/index.html`
- **Failure injection**: `python scripts/ci/failure_injection.py --list`

---

## Future Demos (Planned)

| ID | Title | Milestone |
|---|---|---|
| DEMO-004 | Real MQTT Backbone | M1 |
| DEMO-005 | Evolution Loop | M2 |
| DEMO-006 | Galaxy Viewer | M4 |
