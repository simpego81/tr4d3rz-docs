# Architecture Documentation Workflow

This document explains the automated generation of TR4D3RZ ArchiMate architecture documentation.

## Overview

The documentation system consists of:

1. **Source files**: PlantUML diagrams (`device_*.puml`)
2. **Generated per-device HTML pages**: Interactive ArchiMate views (`docs/*.html`)
3. **Holistic view**: Concentric D3.js visualization (`docs/holistic_view.html`)
4. **Aggregated data**: JSON feed for holistic view (`docs/archimate_data.json`)

## Generation Scripts

### `generate_docs.ps1` — Main Documentation Generator

**Purpose**: Regenerates all device-specific HTML pages from PlantUML source files.

**Usage**:
```powershell
powershell.exe -ExecutionPolicy Bypass -NoProfile -File .\generate_docs.ps1
```

**What it does**:
1. Reads each `device_*.puml` file
2. Extracts ArchiMate elements and relationships
3. Extracts Knowledge Base (KB) metadata from existing HTML files
4. Generates interactive HTML pages with:
   - 4x4 ArchiMate grid (Motivation/Business/Application/Technology × Active/Behavior/Passive/Motivation)
   - SVG relationship arrows
   - Hover interactions (dim/highlight connected elements)
   - Click-to-view element details modal
5. Automatically calls `generate_holistic_data.ps1` at the end

**Output**: `docs/*.html` (one per device)

---

### `generate_holistic_data.ps1` — Holistic View Data Aggregator

**Purpose**: Aggregates all device diagrams into a single JSON feed for the holistic concentric view.

**Usage**:
```powershell
powershell.exe -ExecutionPolicy Bypass -NoProfile -File .\generate_holistic_data.ps1
```

**What it does**:
1. Analyzes all `device_*.puml` files
2. Extracts all ArchiMate elements (ID, type, title)
3. Extracts all relationships (from, to, type, label)
4. For each element/relationship, tracks which devices it appears in
5. Extracts KB metadata (role, tech, type_desc) from existing HTML files
6. Generates `docs/archimate_data.json` with structure:

```json
{
  "metadata": {
    "generated": "2026-05-17 14:30:00",
    "version": "2.0",
    "total_elements": 113,
    "total_relationships": 129
  },
  "elements": {
    "goal_evolve": {
      "title": "Evolve Trading Strategies Autonomously",
      "type": "Motivation_Goal",
      "layer": "Motivation",
      "aspect": "Motivation",
      "type_desc": "ArchiMate Goal — a desired end-state.",
      "role": "The system must autonomously generate...",
      "tech": "Implemented via the Genome Pipeline...",
      "relations": "Realized by the Evolutionary Computing Service...",
      "devices": ["android", "linux", "mimx", "ra8"]
    },
    ...
  },
  "relationships": [
    {
      "from": "proc_evolution",
      "to": "goal_evolve",
      "type": "Realization",
      "label": "",
      "devices": ["android", "linux", "mimx", "ra8"]
    },
    ...
  ]
}
```

**Output**: `docs/archimate_data.json`

---

## Workflow: Making Architecture Changes

### 1. Edit PlantUML Source

Edit one or more `device_*.puml` files:

```plantuml
Application_Component(new_component, "New Component\n(description)")

Rel_Composition_Down(parent_svc, new_component)
```

### 2. Update Knowledge Base (if needed)

If you added new elements, update the corresponding `docs/<device>.html` file's `KB` object:

```javascript
const KB = {
  // ... existing entries ...
  new_component: {
    title: "New Component",
    type: "Application_Component",
    layer: "Application",
    aspect: "Active Structure",
    type_desc: "ArchiMate Application Component element.",
    role: "Detailed description of what this component does in TR4D3RZ.",
    tech: "Implementation technology details.",
    relations: "Relationships with other elements."
  }
};
```

### 3. Regenerate Everything

Run the main generation script:

```powershell
powershell.exe -ExecutionPolicy Bypass -NoProfile -File .\generate_docs.ps1
```

This will:
- ✓ Regenerate all `docs/*.html` files
- ✓ Regenerate `docs/archimate_data.json`
- ✓ Update `holistic_view.html` data feed

### 4. Preview and Commit

Open `docs/index.html` or `docs/holistic_view.html` in a browser to verify changes.

Commit both source and generated files:
```bash
git add device_*.puml docs/*.html docs/archimate_data.json
git commit -m "feat(arch): add new component to X device"
git push
```

GitHub Pages will automatically redeploy the site.

---

## Architecture Consistency Rules

### Element Naming Conventions

| Prefix | Layer | Example |
|--------|-------|---------|
| `goal_*` | Motivation Goal | `goal_evolve` |
| `prin_*` | Motivation Principle | `prin_async` |
| `driver_*` | Motivation Driver | `driver_research` |
| `proc_*` | Business Process | `proc_evolution` |
| `svc_*` | Business/Application Service | `svc_prediction` |
| `data_*` | Business/Application Object | `data_genome` |
| `evo_*` | Evolution components | `evo_mutation` |
| `opt_*` | Optimization components | `opt_tuning` |
| `per_*` | Persistence components | `per_lineage` |
| `obs_*` | Observatory components | `obs_galaxy` |
| `hw_*` | Technology Device | `hw_linux` |
| `rt_*` | Technology Runtime | `rt_rust` |

### Relationship Types (ArchiMate 3.2)

| Relation | Usage | Visual |
|----------|-------|--------|
| `Realization` | Lower layer realizes higher abstraction | Dashed arrow |
| `Composition` | Strong ownership (part-of) | Solid arrow + diamond |
| `Aggregation` | Weak ownership | Solid arrow + hollow diamond |
| `Assignment` | Component assigned to hardware node | Solid arrow + circle |
| `Serving` | Service serves another element | Solid purple arrow |
| `Flow` | Data/control flow | Solid orange arrow |
| `Association` | Generic association | Solid gray arrow |
| `Access` | Read/write access to data | Dashed green arrow |
| `Influence` | Principle/driver influences goal | Dashed gray arrow |

### Layer Separation

- **Motivation Layer**: Goals, Principles, Drivers
- **Business Layer**: Processes, Services, Objects
- **Application Layer**: Services, Components, Functions, Data
- **Technology Layer**: Devices, Nodes, System Software, Artifacts

**Rule**: Relationships can cross layers (Realization, Assignment), but elements stay in one layer.

---

## Troubleshooting

### "Failed to parse KB from docs/X.html"

The script couldn't extract metadata. This happens if:
- The HTML file doesn't exist yet (first-time generation)
- The `KB` object syntax is malformed

**Fix**: Manually add/fix the `KB` object in the HTML file, or let the script generate a skeleton.

### "DISCONNECTED: component_id"

A component exists in the PUML file but has no relationships.

**Fix**: Add at least one `Rel_*` line connecting it to another element.

### Holistic view shows wrong element count

**Fix**: Run `generate_holistic_data.ps1` manually to regenerate the JSON.

### Unicode issues in JSON

**Fix**: The script writes UTF-8 without BOM. If issues persist, check file encoding.

---

## Future Enhancements

- [ ] Validate ArchiMate layer/aspect consistency
- [ ] Auto-generate missing KB entries with templates
- [ ] Detect orphaned elements (no relations)
- [ ] Generate Markdown architecture report
- [ ] PlantUML → SVG rendering for offline viewing
- [ ] Diff tool for architecture changes

---

## References

- [ArchiMate 3.2 Specification](https://pubs.opengroup.org/architecture/archimate3-doc/)
- [PlantUML ArchiMate Guide](https://plantuml.com/archimate-diagram)
- [TR4D3RZ Architecture Docs](https://simpego81.github.io/tr4d3rz-docs/)
