# Debug Intelligence Agent Artifacts

This directory contains outputs from the **Debug Intelligence Agent**.

## Purpose

The Debug Intelligence Agent converts raw observability data (logs, traces, telemetry, demo state) into actionable root cause diagnosis. It operates across all system layers: frontend, backend, APIs, cloud, embedded, databases, message buses.

## Artifact Types

### root_cause_summary.md

Human-readable failure diagnosis produced after debugging sessions.

**Template**:

```markdown
# Root Cause Summary

**Failure ID**: [unique identifier]
**Observed Failure**: [what the user saw]
**Timestamp**: [when it occurred]

## Probable Root Cause

[Causal hypothesis with technical explanation]

**Confidence**: [percentage, e.g., 82%]

## Evidence

- [Event 1 with timestamp and source]
- [Event 2 with timestamp and source]
- [Missing expected event]

## Causal Chain

[Step-by-step flow showing how the failure propagated]

Example:
1. Frontend click → API request
2. API request → DB update
3. DB update → websocket push
4. Websocket push → **UI refresh failure** (root cause: subscription list lost on reconnect)

## Recommended Fix

[Actionable recommendation]

## Observability Gaps

[What made diagnosis difficult — missing logs, no correlation IDs, etc.]
```

---

### debug_audit.md

Assessment of overall system debuggability.

**Contents**:
- Current debugging pain points
- Log/trace quality assessment
- Event correlation capabilities
- Failure pattern frequency (race conditions, timeout chains, retry storms, stale cache, desync)
- Demo observability gaps

**Activation**: Human reports debugging frustration or recurring diagnosis difficulty.

---

### observability_improvements.md

Concrete recommendations for improving debug experience.

**Contents**:
- Better logs (structured logging, correlation IDs)
- Richer demos (event timelines, payload inspectors)
- Replay tools
- Distributed tracing improvements
- Specific instrumentation gaps

**Approval Required**: Recommendations should be reviewed by Architecture Agent before implementation.

---

## Debug Intelligence Features

1. **Event Correlation** — Connect events across layers (frontend → backend → DB → embedded)
2. **Causal Reasoning** — Not just "what happened" but "why it happened"
3. **Failure Pattern Detection** — Recognize recurring classes of failures
4. **Debug UX Improvement** — Proactively recommend observability enhancements

---

## Core Question

> Can the human understand the failure within minutes?

If not, improve debug experience.

---

*Maintainer: Debug Intelligence Agent (Claude Code) — Created: 2026-06-19*
