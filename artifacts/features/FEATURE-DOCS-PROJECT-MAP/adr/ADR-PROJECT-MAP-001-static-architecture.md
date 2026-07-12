# ADR-PROJECT-MAP-001 — Static Site Architecture for GitHub Pages Project Map

**Date**: 2026-07-12  
**Status**: Accepted  
**Author**: Implementation Agent (Claude Code)  
**Feature**: FEATURE-DOCS-PROJECT-MAP  
**Version**: 1.0.0

---

## Context

The TR4D3RZ GitHub Pages documentation currently serves per-device ArchiMate pages and a holistic view. We need to add a progressive project map homepage that presents four interactive views (conceptual ecosystem, physical ecosystem, agent collaboration, roadmap) while maintaining GitHub Pages static hosting constraints.

### Key Requirements

1. **Mobile-first homepage** accessible to non-technical and technical stakeholders
2. **Four progressive disclosure levels**: homepage summaries → area pages → detail pages → evidence sources
3. **Deterministic data pipeline** from authoritative SSOT to validated JSON datasets
4. **Zero backend dependency** — must work on GitHub Pages static hosting
5. **Health and freshness tracking** with explicit provenance and evidence
6. **Debuggability within 2 minutes** for unfamiliar operators

### Design Constraints

- No database, authentication, or server-side rendering
- Must preserve existing device matrix and holistic view pages
- CI/CD must validate without access to local `.ecosystem` directory
- Dataset failures must not break the UI (graceful degradation)
- All data must be traceable to SSOT with timestamps and source refs

---

## Decision

We adopt a **deterministic static site generator architecture** with the following components:

### 1. Data Pipeline (Build Time)

```
┌─────────────┐
│   Collect   │  Read SSOT files (roadmap.yaml, ArchiMate data, 
└──────┬──────┘  Markdown state, Git metadata, sanitized .ecosystem snapshot)
       │
       ▼
┌─────────────┐
│  Normalize  │  Convert to canonical entity/relation model with stable IDs
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Validate   │  Apply JSON Schema, check refs, enums, required fields
└──────┬──────┘  FAIL FAST on critical errors
       │
       ▼
┌─────────────┐
│   Derive    │  Calculate health, freshness, critical path, summaries
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Render    │  Generate JSON datasets + static HTML detail pages
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Publish   │  Atomic replacement of docs/data/generated/
└─────────────┘  Keep last valid snapshot on failure
```

### 2. Published Datasets

All generated in `docs/data/generated/`:

| Dataset | Schema | Purpose |
|---------|--------|---------|
| `conceptual-map.json` | `conceptual-entity.schema.json` | Logical domains and concepts |
| `physical-map.json` | `physical-entity.schema.json` | Components, devices, repos, runtimes |
| `agent-map.json` | `agent-entity.schema.json` | Roles, authorities, handoffs, HRA |
| `roadmap.json` | `roadmap-entity.schema.json` | Milestones, tasks, dependencies, timeline |
| `health-summary.json` | `health-summary.schema.json` | Global health, freshness, staleness indicators |
| `build-manifest.json` | `build-manifest.schema.json` | Schema version, generation time, source hashes, errors, warnings |

### 3. Static UI Architecture

```
docs/
├── index.html                    # New mobile-first homepage (4 summaries)
├── device-matrix.html            # Migrated current homepage
├── maps/
│   ├── conceptual.html           # Full conceptual graph (D3)
│   ├── physical.html             # Full physical topology (D3)
│   ├── agents.html               # Role map + flow map (D3)
│   └── roadmap.html              # Timeline + dependency DAG (D3)
├── details/
│   ├── concepts/<stable-id>.html
│   ├── components/<stable-id>.html
│   ├── roles/<stable-id>.html
│   └── roadmap/<stable-id>.html
├── data/
│   └── generated/                # JSON datasets (atomic publish)
└── shared/
    ├── design-tokens.css
    ├── d3-common.js              # Reusable D3 modules
    └── fallback.js               # Tabular fallback renderer
```

### 4. Technology Stack

| Layer | Technology | Rationale |
|-------|-----------|-----------|
| Data extraction | Python 3 | Portable, testable, rich YAML/JSON libraries |
| Build wrapper | PowerShell | Continuity with current `generate_docs.ps1` |
| Schema validation | JSON Schema Draft 2020-12 | Standard, tooling-rich, CI-friendly |
| Visualization | D3.js v7 | Proven in holistic view, modular, accessible |
| Serialization | JSON | Human-readable, browser-native, schema-validatable |
| CI | GitHub Actions | Native Pages integration, artifact retention |

### 5. SSOT Canonical Sources

| View | Primary SSOT | Integration Sources |
|------|-------------|---------------------|
| Conceptual | ArchiMate model, contracts in `tr4d3rz-docs` | ADRs, specs, knowledge base |
| Physical | ArchiMate model, `specs/node-software-map.md` | Device pages, repo metadata |
| Agents | `.ecosystem/README.md`, mandate, amendment, rules | Sanitized snapshot (allowlist-based) |
| Roadmap | `state/roadmap.yaml` (NEW) | `TASK_QUEUE.md`, feature artifacts, demo registry |
| Health | `state/project_state.md`, risk register, QA reports | Git metadata, build manifest |

**Critical**: `state/roadmap.yaml` becomes the machine-readable SSOT; `state/roadmap.md` becomes a generated view to prevent divergence.

### 6. Health Derivation Rules (Priority Order)

| Priority | Condition | Derived Health |
|----------|-----------|----------------|
| 1 | Status `BLOCKED` OR critical blocker active | `BLOCKED` |
| 2 | Source exceeds freshness threshold AND status not terminal | `STALE` |
| 3 | Required dependency `BLOCKED`/`UNKNOWN`/unresolved OR high risk unmitigated | `AT_RISK` |
| 4 | Status consistent, sources valid, dependencies satisfied, evidence present | `HEALTHY` |
| 5 | Insufficient or conflicting data | `UNKNOWN` |

**Never infer `COMPLETED` without evidence**. Conflicting SSOT produces diagnostic, not silent precedence.

### 7. Failure Modes and Fallbacks

| Failure | Behavior |
|---------|----------|
| Schema validation fails | Build blocked, log `MAP-E001` with file/field/line |
| Duplicate ID or unresolved ref | Build blocked, log `MAP-E002` with entities |
| Sanitized snapshot missing | Use last valid snapshot, show `STALE` badge, log `MAP-E003` |
| Source file unparsable | Error or warning (depending on criticality), log `MAP-E004` |
| Dataset load fails in browser | Static fallback content, diagnostic panel, log `MAP-E005` |
| Critical link broken | Block deploy, report source/target, log `MAP-E006` |
| Partial generation | No publish, keep last valid output, rollback, log `MAP-E007` |
| Dataset exceeds freshness SLA | UI works with `STALE` badge, log `MAP-E008` |

### 8. Local .ecosystem Snapshot Strategy

**Problem**: `.ecosystem/` contains local agent collaboration state (board, decisions, memories) but is excluded from Git and inaccessible to CI.

**Solution**: Two-stage approach

1. **Local Export** (developer machine):
   - Allowlist-based exporter reads `.ecosystem/README.md` + rules
   - Sanitizes: removes private notes, redacts sensitive free text, validates against publishable schema
   - Outputs `artifacts/features/FEATURE-DOCS-PROJECT-MAP/ecosystem-snapshot.json` (committed to Git)
   - Records: generation timestamp, source hashes, schema version

2. **CI Validation** (GitHub Actions):
   - Validates committed snapshot against schema
   - Does NOT access local `.ecosystem`
   - Missing or stale snapshot produces `MAP-E003` warning but does not block deploy if last valid snapshot exists

**Security**: Snapshot schema includes explicit `allowedFields` list; exporter rejects unknown fields to prevent leakage.

---

## Consequences

### Positive

1. **Zero backend cost** — leverages GitHub Pages static hosting
2. **Full traceability** — every datum links to SSOT, timestamp, evidence
3. **Graceful degradation** — UI remains usable even with stale/missing data
4. **Developer-friendly** — Python parsers are unit-testable; PowerShell wrapper is familiar
5. **CI-friendly** — validates schema, links, accessibility without runtime server
6. **Debuggable** — structured logs, error codes, manifest, runbook enable <2min diagnosis

### Negative

1. **No real-time updates** — data refreshes only on build/deploy (mitigated: M1 Observatory provides real-time runtime state; this is for project-level strategic view)
2. **Build-time complexity** — pipeline has 6 phases with schema validation, health derivation, link checking
3. **Manual snapshot export** — developer must run exporter before committing (mitigated: export script is idempotent; CI validates result)

### Risks and Mitigations

| Risk | Trigger | Mitigation |
|------|---------|------------|
| SSOT divergence | Roadmap.md and roadmap.yaml out of sync | roadmap.md becomes generated; schema version tracking |
| Snapshot leak | Private .ecosystem content published | Allowlist schema + exporter validation + QA audit |
| Fragile parsing | Markdown structure changes break collector | Schema-first design; collector unit tests; explicit error codes |
| Stale data presented as current | Old snapshot served without warning | Freshness badge on homepage; build manifest tracks age |
| Legacy page regression | Device matrix links break | Link checker in CI; migration preserves all existing routes |
| Partial publish | Build crashes mid-render | Staging directory + atomic publish; rollback on failure |
| Commit pollution | Feature changes mixed with unrelated edits | Isolated branch/worktree; file allowlist per task |

All risks have explicit veto conditions in `risks.md`.

---

## Alternatives Considered

### A. Dynamic Backend (Rejected)

- **Pros**: Real-time updates, no build step, simpler frontend
- **Cons**: Hosting cost, maintenance burden, authentication/CORS complexity, breaks GitHub Pages constraint
- **Rejection reason**: Violates "zero backend" architectural principle for documentation site

### B. Client-Side SSOT Parsing (Rejected)

- **Pros**: No build pipeline, always fresh
- **Cons**: Exposes raw SSOT files (including .ecosystem), fragile browser parsing, no schema validation, poor UX on slow connections
- **Rejection reason**: Cannot sanitize .ecosystem; brittle; violates "validated data" requirement

### C. Markdown-Only (Rejected)

- **Pros**: Simple, familiar, no tooling
- **Cons**: No interactive graphs, poor mobile UX, manual cross-linking, no health derivation, no drill-down
- **Rejection reason**: Does not meet "progressive disclosure" and "interactive maps" requirements

---

## Migration Path

1. **M0 (PMAP-00, PMAP-01)**: Approve ADR, define schemas, update SSOT
2. **M1 (PMAP-02–06)**: Implement pipeline, validate with fixtures
3. **M2 (PMAP-07–09)**: Build UI shell, homepage, detail templates (using fixtures from M1)
4. **M3 (PMAP-10–13)**: Implement four D3 maps
5. **M4 (PMAP-14–15)**: Migrate device-matrix.html, add CI gates
6. **M5 (PMAP-16–19)**: Runbook, QA, demo, audit, closure

Each milestone has explicit exit gate; M1 must complete before M2 frontend work begins (contract-first design).

---

## Compatibility Notes

- Preserves all existing `.puml`, device pages, `holistic_view.html`
- `docs/index.html` replaced only after preview approval
- All generated files include schema version for future migrations
- Design tokens and D3 modules enable future brand updates without code changes

---

## References

1. `artifacts/features/FEATURE-DOCS-PROJECT-MAP/spec.md` — Feature specification
2. `artifacts/features/FEATURE-DOCS-PROJECT-MAP/tasks.yaml` — Task backlog
3. `artifacts/features/FEATURE-DOCS-PROJECT-MAP/risks.md` — Risk register
4. `protocols/MVP_INTERFACE_CONTRACTS.md` — CBOR contracts (for runtime system)
5. `adr/ADR-0002-technology-stack.md` — Overall TR4D3RZ tech stack

---

**Approval**: Architect — 2026-07-12  
**Implementation Start**: PMAP-02 (after schema publication)
