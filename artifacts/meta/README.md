# Meta-Optimizer Agent Artifacts

This directory contains outputs from the **Meta-Optimizer Agent** (System Optimization Agent).

## Purpose

The Meta-Optimizer Agent analyzes the AI ecosystem itself, not the product. It detects inefficiencies, rework loops, convergence failures, and proposes structural improvements to the multi-agent collaboration workflow.

## Artifact Types

### convergence_audit.md

Periodic assessment of ecosystem convergence quality.

**Contents**:
- Current convergence metrics (from `state/meta_metrics.md`)
- Detected inefficiencies (excessive rework, architecture oscillation, iteration bloat)
- Root causes of poor convergence
- Systemic bottlenecks

**Activation**: Periodic review or when metrics exceed thresholds.

---

### optimization_proposals.md

Concrete proposals for improving ecosystem efficiency.

**Contents**:
- TRIZ contradiction analysis (e.g., autonomy vs coherence)
- De Bono lateral thinking provocations (e.g., "Po: Remove QA entirely")
- Systems thinking recommendations (global optimization strategies)
- Proposed changes to: prompts, workflows, validation rules, handoff protocols

**Approval Required**: Manus must approve before implementation.

---

### workflow_changes.md

Log of applied workflow modifications.

**Contents**:
- Change description
- Rationale (why convergence was failing)
- Expected impact on metrics
- Actual impact (post-implementation measurement)

**Maintained by**: Meta-Optimizer Agent

---

## Methods Used

1. **TRIZ** — Contradiction resolution (e.g., "More autonomy → less coherence" → eliminate contradiction via bounded autonomy, explicit artifact schemas)
2. **Edward De Bono Lateral Thinking** — Provocation, inversion, random entry for paradigm shifts
3. **Systems Thinking** — Global optimization, feedback loop analysis

---

## Core Question

> Is the multi-agent system converging toward the best solution fast enough?

If not, intervene.

---

*Maintainer: Meta-Optimizer Agent (Claude Code) — Created: 2026-06-19*
