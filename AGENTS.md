# AGENTS.md — TR4D3RZ Agent Architecture

> **Model**: Single Orchestrator (Claude Code) + ephemeral specialized subagents (Option C, adopted 2026-07-15)
> **Organizational framework**: [Software House AI](https://github.com/simpego81/software-house-ai)
> **Role definitions**: `agents/` (source of truth for each implementation role)
> **Last updated**: 2026-07-25 — harmonization with Software House AI framework

---

## 0. Software House AI Integration

TR4D3RZ operates under the **two-level model** decided 2026-07-25:

| Level | Framework | Scope | When to use |
|-------|-----------|-------|-------------|
| **Organizational** | Software House AI — 12-step cycle | Architectural decisions, feature specifications, protocol changes, cross-repo contracts | New ADR, MQTT protocol change, new component design, changes to AGENTS.md or CONSTITUTION |
| **Implementation** | TR4D3RZ — subagent workflow | Day-to-day coding, testing, debugging, documentation, CI/CD | Implementing an already-specified feature, fixing bugs, running PQM audits |

**Rule:** Use the Software House 12-step cycle when the output of the decision will be an ADR, a spec change, or a modification to shared protocols. Use the TR4D3RZ subagent workflow when the output is code, test results, or a documentation update.

**Memory boundary:**
- `.swhouse/memory/` → organizational decisions (architecture, cross-repo patterns, major errors at architectural level)
- `COMMUNICATION/IMPLEMENTATION_LOG.md` → implementation task history (code-level)
- `DASHBOARD.md` → session re-entry snapshot
- `state/meta_metrics.md` → implementation quality metrics

### Role mapping: Software House AI ↔ TR4D3RZ

| Software House Agent | Step | Maps to TR4D3RZ role(s) | Notes |
|---------------------|------|------------------------|-------|
| COORDINATOR | 1 | Orchestratore | Opens SW-H cycles for architectural decisions; Orchestrator manages task flow for implementation |
| PRODUCT OWNER | 2 | Owner (human) | Feature value decisions remain with the human operator |
| ARCHITECT | 3 | Architect subagent | SW-H for cross-repo architectural decisions; TR4D3RZ Architect for spec writing |
| EXPLORER | 4 | (none) | No direct TR4D3RZ equivalent; Orchestrator generates alternatives when needed |
| CRITIC | 5 | Reviewer subagent | SW-H Critic on architectural proposals; TR4D3RZ Reviewer on code quality |
| DESTROYER | 6 | Reviewer + Debugger | SW-H Destroyer on architectural security/resilience; TR4D3RZ for runtime failures |
| BUILDER | 7 | Planner + Developer | SW-H Builder produces specs and plans; TR4D3RZ Developer writes code |
| OPTIMIZER | 8 | PQM (partially) | SW-H Optimizer simplifies architectural solutions; PQM enforces implementation quality |
| SCIENTIST | 9 | Tester | SW-H Scientist verifies architectural hypotheses; Tester validates code behavior |
| LIBRARIAN | 10 | Documentation Agent | SW-H Librarian → `.swhouse/memory/`; Documentation Agent → TR4D3RZ state files |
| EVOLUTION MASTER | 11 | PQM + Meta-Optimizer | SW-H at organizational process level; Meta-Optimizer at implementation process level |
| ARBITER | 12 | Owner (human) | Final architectural decisions require Owner approval |

---

## 1. Hierarchy and Actor Model

```
Owner (human)
  ↕ approves: ADRs, protocol changes, priority changes, component removal
  ↕ runs Software House 12-step cycle for architectural decisions
  
Claude Code [ORCHESTRATOR — permanent role]
  ├── Reads CONSTITUTION.md + AGENTS.md + TASK_QUEUE.md + current_task.md each session
  ├── Selects task → determines phase sequence → spawns subagents
  ├── Integrates outputs → updates state files
  ├── Triggers PQM every 3 tasks or on threshold breach
  └── Proposes architectural decisions to Owner (via Software House cycle or direct proposal)
  
Specialized subagents [ephemeral — spawned per phase]
  ├── Planner          [Plan-type]          — incomplete spec, new feature
  ├── Architect        [claude]             — ADR, protocol, new contract
  ├── Developer        [claude + worktree]  — implementation
  ├── Reviewer         [code-reviewer]      — adversarial QA post-implementation
  ├── Debugger         [claude]             — test failure, runtime anomaly
  ├── Tester           [claude]             — validation before COMPLETED
  ├── Documentation    [claude]             — state/ArchiMate sync (MANDATORY)
  ├── PQM              [claude]             — Constitution compliance audit
  ├── Pipeline Mgr     [claude] STUB        — GitHub Actions CI/CD (post-M1)
  └── Deployment Mgr   [claude] STUB        — device deployment (post-M1)
```

**Fundamental rule**: every role has its complete definition in `agents/<role>.md`. The Orchestrator reads the role file before constructing each brief.

---

## 2. Role Definitions

| File | Role | Subagent type | Status |
|------|------|---------------|--------|
| [agents/orchestrator.md](agents/orchestrator.md) | Orchestrator | Claude Code primary | ACTIVE |
| [agents/planner.md](agents/planner.md) | Planner | Plan-type | ACTIVE |
| [agents/architect.md](agents/architect.md) | Architect | claude | ACTIVE |
| [agents/developer.md](agents/developer.md) | Developer | claude + worktree | ACTIVE |
| [agents/reviewer.md](agents/reviewer.md) | Reviewer | code-reviewer | ACTIVE |
| [agents/debugger.md](agents/debugger.md) | Debugger | claude | ACTIVE |
| [agents/tester.md](agents/tester.md) | Tester | claude | ACTIVE |
| [agents/documentation.md](agents/documentation.md) | Documentation Agent | claude | ACTIVE |
| [agents/pqm.md](agents/pqm.md) | Process Quality Manager | claude | ACTIVE |
| [agents/pipeline-manager.md](agents/pipeline-manager.md) | Pipeline Manager | claude | STUB |
| [agents/deployment-manager.md](agents/deployment-manager.md) | Deployment Manager | claude | STUB |

---

## 3. Repository Scope

| Repository | Scope | Orchestrator may delegate to |
|------------|-------|------------------------------|
| `tr4d3rz-docs` | SSOT, architecture, specs, agents/, state/ | Documentation Agent, PQM |
| `tr4d3rz-core` | Shared types, FSM runtime | Developer + Reviewer |
| `tr4d3rz-messaging` | MQTT client, gateway | Developer + Reviewer |
| `tr4d3rz-evolution` | Mutation, fitness, niche | Developer + Reviewer |
| `tr4d3rz-persistence` | Event sourcing, SQLite | Developer + Reviewer |
| `tr4d3rz-observatory` | UI, visualization, replay | Developer + Reviewer |
| `tr4d3rz-embedded` | ESP8266, STM32 | Developer (no_std) |

**Protocol rule**: no repository may change a shared contract without updating `protocols/` first.

---

## 4. Phase Sequences by Task Type

| Task type | Mandatory phases | Optional phases |
|-----------|-----------------|-----------------|
| New feature (spec absent) | Planner → Architect → Developer → Documentation | Reviewer (if critical) |
| Implementation (spec present) | Developer → Documentation | Reviewer, Tester |
| Bug fix | Debugger → Developer → Tester → Documentation | Reviewer |
| ADR / protocol change | **Software House 12-step cycle** → Architect | — |
| Pre-release validation | Tester → PQM | — |
| Documentation sync only | Documentation | — |
| Architectural decision | **Software House 12-step cycle** | — |

---

## 5. Session Handover Protocol

### Session start

Read in order:
1. `docs/CONSTITUTION.md` (project-level rules)
2. `AGENTS.md` (this file — agent model + Software House integration)
3. `COMMUNICATION/TASK_QUEUE.md` (active tasks)
4. `COMMUNICATION/TASKS/current_task.md` (current task details)
5. `.swhouse/cycles/` — check if a Software House cycle is open

If DASHBOARD stale > 2 days: update before any other task.

### End of implementation task

1. `COMMUNICATION/TASKS/current_task.md` → COMPLETED
2. `COMMUNICATION/IMPLEMENTATION_LOG.md` → new entry
3. `COMMUNICATION/TASK_QUEUE.md` → status updated
4. Spawn Documentation Agent if task changed component state

### End of Software House cycle

1. Move `.swhouse/cycles/current.md` → `cycles/archive/cycle-NNN.md`
2. Update `.swhouse/reputation/scores.yaml`
3. Update `.swhouse/metrics/summary.yaml`
4. Commit `.swhouse/` state to git

### End of session

Update `DASHBOARD.md` with current state snapshot.

---

## 6. Proposal → Owner Approval Protocol

**Requires Owner approval (trigger Software House cycle or direct proposal):**
- New ADRs (architectural change)
- Modifications to `protocols/` (shared contracts)
- Priority changes between milestone tasks
- Removal of existing components
- Modifications to `CONSTITUTION.md` or `AGENTS.md`

**Proceed autonomously:**
- State file updates (DASHBOARD, current_task, IMPLEMENTATION_LOG)
- Implementation of already-approved tasks in TASK_QUEUE
- Documentation inconsistency fixes
- Spawning subagents for standard tasks
- Detail updates to `agents/` files (new roles → propose; detail updates → autonomous)

---

## 7. Secret Management

- `.env.test` with sensitive variables always in `.gitignore`
- No agent commits `.env*` files
- Variable naming convention: `TR4D3RZ_<NAME>` in `.env.test` at target repo root

---

## 8. Meta-Optimizer Activation Triggers

The Orchestrator activates Meta-Optimizer mode (improvement proposal to PQM) when:

- Spec revised >3 times for the same feature
- Rework ratio >0.4 on a task (PARTIAL output + retry >1)
- Task COMPLETED without a corresponding git commit
- Session requires >15 min to understand current state
- PQM finds >3 HIGH findings in a single audit
- Owner explicitly requests optimization

**Output**: `artifacts/meta/convergence_audit_<date>.md` + `artifacts/meta/optimization_proposals.md`

---

*Maintainer: Claude Code (Orchestrator) — Updated: 2026-07-25*
