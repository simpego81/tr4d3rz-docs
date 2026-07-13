# TR4D3RZ Multi-Agent Ecosystem — Quick Reference

**Last Updated**: 2026-06-19

---

## Agent Roles & Responsibilities

| Agent | Role | Repositories | Can Write Code? |
|---|---|---|---|
| **Manus** | Chief Architect & Orchestrator | `tr4d3rz-docs` (coordination only) | ❌ NO |
| **Claude Code** | Backend + Frontend Developer + Meta-Optimizer + Debug Intelligence + QA | `tr4d3rz-core`, `tr4d3rz-messaging`, `tr4d3rz-evolution`, `tr4d3rz-persistence`, `tr4d3rz-observatory` | ✅ Yes |
| **GitHub Copilot** | Embedded Developer & Validator | `tr4d3rz-embedded` | ✅ Yes |

---

## Meta-Layer Agents (Orthogonal to Features)

### Meta-Optimizer Agent (Claude Code)

**Purpose**: Optimize the AI ecosystem itself  
**Methods**: TRIZ, De Bono lateral thinking, systems thinking  
**Core Question**: Is the multi-agent system converging fast enough?

**Activation Triggers**:
- Excessive rework
- Architecture oscillation
- Slow progress
- Quality plateau

**Deliverables**:
- `artifacts/meta/convergence_audit.md`
- `artifacts/meta/optimization_proposals.md`
- `state/meta_metrics.md`

---

### Debug Intelligence Agent (Claude Code)

**Purpose**: Optimize human debugging experience  
**Scope**: All layers (frontend, backend, APIs, cloud, embedded, DB, message buses)  
**Core Question**: Can the human understand the failure within minutes?

**Activation Triggers**:
- Debugging frustration
- Unclear root cause
- Noisy logs
- Insufficient demos

**Deliverables**:
- `artifacts/debug/root_cause_summary.md`
- `artifacts/debug/debug_audit.md`
- `artifacts/debug/observability_improvements.md`

---

## Before Starting Any Task

1. **Check task queue**: `COMMUNICATION/TASK_QUEUE.md`
2. **Read specs**: `specs/[component]/`
3. **Review protocols**: `protocols/`
4. **Check ADRs**: `adr/`
5. **Read shared state**: `state/` (especially `project_state.md`, `meta_metrics.md`)

---

## Task Workflow

1. Update `COMMUNICATION/TASKS/current_task.md` (status: `IN_PROGRESS`)
2. Implement according to specifications
3. Document in `COMMUNICATION/IMPLEMENTATION_LOG.md`
4. Mark `COMPLETED` only after testing/validation
5. Update `COMMUNICATION/PROJECT_STATE.md`

---

## Convergence Metrics (Meta-Optimizer)

| Metric | Threshold | Meaning |
|---|---|---|
| **Requirement Churn** | >3 revisions | Spec instability |
| **Rework Ratio** | >0.4 | Inefficient iterations |
| **Review Cycle Count** | >2 cycles | Poor convergence |
| **Demo Validation Time** | >15 min | Observability gap |

**Tracked in**: `state/meta_metrics.md`

---

## Artifact Structure

```
artifacts/
├── features/          # Feature-specific deliverables
│   └── FEATURE-XXX/
│       ├── spec.md
│       ├── tasks.yaml
│       ├── architecture.md
│       └── qa_report.md
├── meta/              # Meta-Optimizer Agent outputs
│   ├── convergence_audit.md
│   ├── optimization_proposals.md
│   └── workflow_changes.md
└── debug/             # Debug Intelligence Agent outputs
    ├── root_cause_summary.md
    ├── debug_audit.md
    └── observability_improvements.md
```

---

## State Files

```
state/
├── project_state.md    # Executive summary, priorities, metrics
├── roadmap.md          # Milestone tracking
├── decisions.md        # Key decisions log
├── risks.md            # Risk register
├── demo_registry.md    # Demo inventory
└── meta_metrics.md     # Convergence metrics (Meta-Optimizer)
```

---

## Protocol Change Rule

**CRITICAL**: No repository may change a shared protocol or data contract without updating `tr4d3rz-docs/protocols/` first.

---

## Definition of Done (Demo-Driven Development)

A feature is complete only if:

- ✅ Requirement refined
- ✅ Architecture approved
- ✅ Code implemented
- ✅ Tests pass
- ✅ **Demo available**
- ✅ **Demo validated**
- ✅ Documentation updated
- ✅ UML updated
- ✅ Debug instructions updated
- ✅ Failure scenarios considered

---

## Mutual Verification Protocol

> "The previous agent may have made mistakes."

1. **Read Shared State** — Always check `state/` before acting
2. **Verify Inputs** — Reject vague specs
3. **Verify Outputs** — QA must attempt to break implementation
4. **Observable Handoff** — Use `artifacts/features/` for exchanges
5. **Meta-Layer Supervision** — Meta-Optimizer and Debug Intelligence agents can challenge anyone

---

## Key Documents

- **Architecture**: `ARCHITECTURE_WORKFLOW.md`, `archimate_diagram_v2.puml`
- **Agents**: `AI_ROLES.md`, `AGENTS.md`, `META_LAYER_GUIDE.md`
- **Protocols**: `protocols/mqtt-topic-structure.md`
- **Specs**: `specs/[core|messaging|evolution|observatory|persistence|embedded]/`
- **ADRs**: `adr/ADR-NNNN-title.md`
- **Milestones**: `milestones/M[0-5]/`

---

## Success Criteria

**The human operator should be able to say**:

> "I understand what the system is doing, why it behaves this way, and I can validate progress quickly."

---

*Maintained by: Manus (Chief Architect) — Last Updated: 2026-06-19*
