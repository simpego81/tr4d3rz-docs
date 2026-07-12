# Schema Changelog — FEATURE-DOCS-PROJECT-MAP

All notable changes to the project map data contract schemas will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and schema versions adhere to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - 2026-07-12

### Added

- **common-entity.schema.json** v1.0.0
  - Base schema for all entities with required fields: `id`, `kind`, `name`, `summary`, `status`, `health`, `owners`, `dependencies`, `blockers`, `updated_at`, `evidence`, `source_refs`, `detail_url`
  - Status vocabulary: `PLANNED`, `READY`, `IN_PROGRESS`, `BLOCKED`, `COMPLETED`, `DEPRECATED`, `UNKNOWN`
  - Health vocabulary: `HEALTHY`, `AT_RISK`, `BLOCKED`, `STALE`, `UNKNOWN`
  - Ownership model with role/agent pairs
  - Blocker tracking with severity levels
  - Evidence tracking with typed links (demo, commit, qa_report, adr, spec, etc.)
  - Source provenance with file paths and SHA-256 hashes
  - Stable ID pattern: `^[a-z0-9][a-z0-9-]*[a-z0-9]$` (kebab-case)

- **roadmap.schema.json** v1.0.0
  - Extends common-entity for milestones and tasks
  - Milestone-specific fields: `outcome`, `start_date`, `end_date`, `tasks`, `critical_path`
  - Task-specific fields: `milestone_id`, `acceptance_criteria`, `outputs`, `estimated_effort`, `actual_completion_date`
  - Nullable date fields to represent unscheduled work (never invented)
  - T-shirt size effort estimation (XS → XXL)

- **build-manifest.schema.json** v1.0.0
  - Build metadata schema for docs/data/generated/build-manifest.json
  - Tracks: schema version, generation timestamp, generator version, git commit
  - Source file inventory with SHA-256 hashes and read timestamps
  - Dataset inventory with entity counts and schema versions
  - Error tracking with MAP-E001–MAP-E008 codes and file/field/line location
  - Warning tracking with MAP-W001+ codes
  - Last valid snapshot reference for rollback
  - Phase duration metrics for performance monitoring
  - Freshness status indicator (FRESH/STALE/UNKNOWN)

- **CHANGELOG.md** (this file)
  - Schema versioning and migration notes

### Design Decisions

- **Strict schema validation**: All datasets must validate against schemas before publish
- **Stable IDs**: Kebab-case pattern enforced to enable predictable deep-linking
- **No percentage completion**: Only explicit status values; `COMPLETED` requires evidence
- **Nullable vs. omitted**: Missing dates are `null` (explicit absence) not omitted (ambiguous)
- **Provenance first**: Every entity must declare `source_refs` with file hashes for traceability
- **Graceful degradation**: Health can be `UNKNOWN` when data is insufficient; UI must handle this

### Migration Notes

This is the initial schema version. No migration needed.

---

## Future Versions

### Schema Compatibility Rules

- **MAJOR version** (x.0.0): Breaking changes requiring consumer updates
  - Removing required fields
  - Changing enum values
  - Renaming properties
  - Changing data types

- **MINOR version** (1.x.0): Backward-compatible additions
  - Adding optional fields
  - Adding new enum values (consumers should handle unknown values gracefully)
  - Extending nested object schemas

- **PATCH version** (1.0.x): Non-functional changes
  - Documentation improvements
  - Example updates
  - Description clarifications

### Planned Enhancements (Future)

- Additional entity kinds: `protocol`, `adr`, `demo`, `device`, `repository` (MINOR)
- Relationship typing beyond dependency array (MINOR or MAJOR depending on backward compatibility)
- Multi-language summary support (MINOR)
- Structured risk tracking within entities (MINOR)

---

## References

- ADR-PROJECT-MAP-001: Static Site Architecture for GitHub Pages Project Map
- FEATURE-DOCS-PROJECT-MAP/spec.md: Feature specification
- FEATURE-DOCS-PROJECT-MAP/tasks.yaml: Task PMAP-01 acceptance criteria
