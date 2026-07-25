---
date: 2026-07-25
cycle: N/A
title: Software House AI framework integration — two-level model
status: active
---

## Context

TR4D3RZ had its own agent architecture (Option C: Orchestrator + 10 subagents) with its own constitution, state management files, and subagent protocol. The Software House AI framework (github.com/simpego81/software-house-ai) was created to govern AI-driven software organizations. TR4D3RZ needed to be harmonized with the new framework.

## Decision

Three decisions were made (2026-07-25):

**D1 — Two-level model (Role coexistence)**
Software House AI's 12-agent organizational cycle governs architectural decisions. TR4D3RZ's 10-role subagent workflow governs implementation execution. The two levels do not compete — they address different scopes.

Trigger for Software House cycle: new ADR, protocol change, feature specification, modification to AGENTS.md or CONSTITUTION.md.
Trigger for TR4D3RZ workflow: implementing a specified feature, fixing bugs, running PQM audits, documentation sync.

**D2 — Memory coexistence (Option A)**
`.swhouse/memory/` holds organizational-level knowledge (architectural decisions, cross-repo patterns, major errors at architectural level). TR4D3RZ state files (IMPLEMENTATION_LOG, DASHBOARD, TASK_QUEUE, meta_metrics) continue unchanged for implementation-level state. No migration planned.

See `.swhouse/BOUNDARY.md` for the detailed boundary definition.

**D3 — AGENTS.md as mapping document**
`tr4d3rz-docs/AGENTS.md` was reorganized to include a §0 section that explicitly maps Software House AI agents to TR4D3RZ subagent roles. The detailed operational specifications remain in `agents/*.md`.

## Rationale

The two-level model preserves the mature, working TR4D3RZ implementation workflow while adding organizational governance via Software House AI. Migrating all state to `.swhouse/` would have destroyed the existing PQM audit trail and meta_metrics history without adding value. AGENTS.md as a mapping document creates a single point of reference for anyone needing to understand how the two frameworks relate.

## Consequences

- The Software House 12-step cycle is now the prescribed path for architectural decisions in TR4D3RZ
- `.swhouse/` must be committed to tr4d3rz-docs and kept in sync via git
- `AGENTS.md §0` is the authoritative source for the two-level model boundary

## Confidence

High. Decision was made by Owner with full context of both frameworks.
