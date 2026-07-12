# Privacy Validation Report — Ecosystem Snapshot Exporter

**Date**: 2026-07-12  
**Schema Version**: 1.0.0  
**Exporter**: `scripts/export_ecosystem_snapshot.py`  
**Output**: `artifacts/features/FEATURE-DOCS-PROJECT-MAP/ecosystem-snapshot.json`

---

## 1. Validation Summary

✅ **PASS**: No secret, private free text, or unsupported fields are published.

- Schema validation: PASS (v1.0.0)
- Allowlist enforcement: PASS
- Excluded fields: 6 categories
- Agents exported: 4 (TEMPLATE_agent excluded)
- Source hash: Recorded for traceability

---

## 2. Allowlist-Based Sanitization

The exporter uses a **strict allowlist** of publishable fields:

| Field | Type | Rationale |
|-------|------|-----------|
| `agent_id` | string | Public identifier (derived from filename) |
| `role` | enum | Public role from AGENTS.md |
| `repositories` | array | Public repository ownership |
| `last_update` | timestamp | Operational metric, no sensitive content |
| `current_task` | string | Task ID only (e.g., "M1-T3"), not full description |
| `confidence_level` | integer | Aggregate metric (0-100) |
| `blockers` | array | Sanitized: generic description + owner + status (no free text) |
| `vetos_issued_count` | integer | Count only, no veto details |
| `vetos_received_count` | integer | Count only, no veto details |

---

## 3. Excluded Fields (Private/Sensitive)

The following fields from agent boards are **NEVER exported**:

1. **`context_assumptions`**: May contain internal assumptions about architecture or stakeholders
2. **`recent_decisions`**: May reveal strategic reasoning or decision rationale
3. **`open_questions`**: Exposes uncertainty to external stakeholders
4. **`uncertainty_sources`**: Private diagnostic information
5. **`collaboration_surface`**: Inter-agent communication details
6. **`key_dependencies`**: May contain implementation-specific dependencies

These fields are listed explicitly in the snapshot under `excluded_fields` for transparency.

---

## 4. Validation Steps

### Step 1: Schema Compliance

- ✅ Output validates against `ecosystem-snapshot.schema.json` v1.0.0
- ✅ All required fields present: `schema_version`, `generated_at`, `source_hash`, `agents`, `rules_summary`

### Step 2: Content Sanitization

- ✅ No free-text notes from boards included
- ✅ Blocker descriptions are generic (from board template structure, not free text)
- ✅ Veto details are counts only (no dates, no reasons, no affected agents)
- ✅ TEMPLATE_agent excluded (contains placeholder data)

### Step 3: Source Provenance

- ✅ `source_hash`: SHA-256 hash of .ecosystem directory state recorded
- ✅ `generated_at`: ISO 8601 timestamp recorded
- ✅ Snapshot can be traced back to specific .ecosystem state

### Step 4: Unknown Field Rejection

- ✅ Exporter uses explicit allowlist - unknown fields are **never** included
- ✅ `additionalProperties: false` in schema enforces no undocumented fields

---

## 5. Sample Validation Output

Current snapshot (2026-07-12):

```json
{
  "schema_version": "1.0.0",
  "generated_at": "2026-07-12T15:52:14.505437Z",
  "source_hash": "4fe58c5ad596ecf7f8439e8b75c3c0ec5c31978e1703cff0f3793ac48d1e588e",
  "agents": [
    {
      "agent_id": "claude-code",
      "role": "Implementation Agent",
      "repositories": ["tr4d3rz-core", "tr4d3rz-messaging", "tr4d3rz-evolution", "tr4d3rz-persistence"],
      "last_update": "2026-07-10T19:30:00+00:00",
      "current_task": null,
      "confidence_level": 90,
      "blockers": [],
      "vetos_issued_count": 1,
      "vetos_received_count": 1
    },
    ...
  ],
  "rules_summary": {
    "veto_gates": [...],
    "artifact_handoff": {...},
    "hra_protocol": {...}
  },
  "excluded_fields": [
    "context_assumptions",
    "recent_decisions",
    "open_questions",
    "uncertainty_sources",
    "collaboration_surface",
    "key_dependencies"
  ]
}
```

**Validation**: No sensitive content detected.

---

## 6. Missing Snapshot Handling

If `.ecosystem` directory is not available (e.g., on CI), the exporter:

- Returns exit code 1 (non-fatal)
- Prints explanatory message
- CI will use the last committed snapshot instead
- UI will show `STALE` badge with `MAP-E003` diagnostic code

**Test**: Missing .ecosystem does NOT break the build pipeline.

---

## 7. Recommendations

1. **QA Review**: Have GitHub Copilot (QA Validator) review the first published snapshot for unintended leakage
2. **Schema Evolution**: When adding new fields to agent boards, explicitly decide: allowlist or excluded?
3. **Periodic Audit**: Review `excluded_fields` list quarterly to ensure it remains comprehensive

---

## 8. Approval

**Validated by**: Claude Code (Implementation Agent)  
**Date**: 2026-07-12  
**Status**: ✅ APPROVED for PMAP-03 acceptance

**Next Step**: QA validation in PMAP-17 (independent review by GitHub Copilot)
