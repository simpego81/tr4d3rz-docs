# TR4D3RZ Knowledge Base — Unified Index

**Maintainer**: Librarian Agent (Claude Code / Antigravity)  
**Purpose**: Single entry point to all ecosystem knowledge  
**Last Updated**: 2026-07-11  
**Status**: ACTIVE

---

## Purpose

The Knowledge Base is a **primary product** of the TR4D3RZ AI-Native Collaborative Software Studio. It evolves continuously and serves as the single source of truth for:

- Architectural decisions and principles
- Operational procedures and capabilities
- Shared agent memories and learnings
- Project status and progress tracking
- Technical specifications and contracts

**Target**: Any agent (or human) should quickly find needed knowledge and trust it's current.

---

## Quick Navigation

### For Rapid Project Re-Entry

→ **[Dashboard](DASHBOARD.md)** — Architecture health, roadmap, current work, risks (target: <5 min understanding)

### For Understanding Roles and Workflows

→ **[AI Roles](AI_ROLES.md)** — Specialized agent role definitions  
→ **[Agents](AGENTS.md)** — Repository assignments and operational rules  
→ **[Meta-Layer Guide](META_LAYER_GUIDE.md)** — Meta-Optimizer and Debug Intelligence agents

### For Current Work

→ **[Task Queue](COMMUNICATION/TASK_QUEUE.md)** — Current milestone and task priorities  
→ **[Project State](state/project_state.md)** — Overall project status

---

## Knowledge Categories

### 1. Architecture

**Purpose**: Understand system structure and principles

| Resource | Description | Audience |
|---|---|---|
| [README.md](README.md) | Project vision, repository map, architectural principles | All agents, newcomers |
| [QUICK_REFERENCE.md](QUICK_REFERENCE.md) | Quick reference card for all agents | All agents |
| [AI_AGENT_DOCUMENTATION.md](AI_AGENT_DOCUMENTATION.md) | Instructions for AI agents working on TR4D3RZ | All agents |
| [Architecture Workflow](ARCHITECTURE_WORKFLOW.md) | Documentation generation workflow (PlantUML → HTML) | Manus, Documentation Agent |
| [ADRs](adr/) | Architectural Decision Records (immutable once accepted) | Architecture Agent, Manus |

**Key Principles** (from [README.md](README.md)):
1. Open-Ended Evolution (evolutionary pressure, not rigid limits)
2. Asynchronous Distributed Ecology (no global synchronization)
3. Emergent Specialization (niche domination, not universal strategies)
4. Cooperative Signaling (event-based, not direct references)
5. Distributed Observability (serializable, replayable, visualizable)

---

### 2. Specifications

**Purpose**: Define interfaces and contracts before implementation

| Resource | Description | Owner |
|---|---|---|
| [specs/](specs/) | Technical specifications per component (core, messaging, evolution, observatory, persistence, embedded) | Architecture Agent |
| [protocols/](protocols/) | Protocol definitions and data contracts (MQTT topic structure, CBOR schemas) | Architecture Agent |
| [SPEC_MASTER.md](COMMUNICATION/SPEC_MASTER.md) | MVP interface contracts v0.1 | Manus |

**CRITICAL RULE**: No repository may change a shared protocol/contract without updating `protocols/` first.

---

### 3. Roadmap and Milestones

**Purpose**: Track progress and plan future work

| Resource | Description | Owner |
|---|---|---|
| [state/roadmap.md](state/roadmap.md) | **Canonical roadmap** — Milestone definitions (M0-M5) | Manus |
| [milestones/](milestones/) | Detailed milestone plans | Manus |
| [TASK_QUEUE.md](COMMUNICATION/TASK_QUEUE.md) | Current milestone (M1) task breakdown and dependencies | Manus |

**Current Milestone**: M1 — Foundational Backbone Single RPi2

---

### 4. Design Decisions

**Purpose**: Understand why the system is designed this way

| Resource | Description | Status |
|---|---|---|
| [ADR-0001](adr/ADR-0001-repository-structure.md) | Repository structure (7 repositories) | ACCEPTED |
| [ADR-0002](adr/ADR-0002-technology-stack.md) | Technology stack (Rust, WASM, MQTT, CBOR) | ACCEPTED |
| [ADR-0003](adr/ADR-0003-mqtt-broker.md) | MQTT broker choice (NanoMQ → Mosquitto for RPi 1) | ACCEPTED |
| [ADR-0004](adr/ADR-0004-ohlcv-data-contract.md) | OHLCV data contract (CBOR serialization) | ACCEPTED |
| [.ecosystem/DECISIONS.md](.ecosystem/DECISIONS.md) | Operational decisions log (veto enforcement, location, etc.) | ACTIVE |

**Format**: ADRs are immutable once accepted. Create new ADR to supersede, don't edit original.

---

### 5. Project Status

**Purpose**: Understand current state and progress

| Resource | Description | Update Frequency |
|---|---|---|
| **[state/project_state.md](state/project_state.md)** | **Canonical project status** | After each task completion |
| [state/risks.md](state/risks.md) | Project risks and mitigations | As risks identified |
| [state/decisions.md](state/decisions.md) | Historical decisions log | As decisions made |
| [state/demo_registry.md](state/demo_registry.md) | Completed demos catalog | After each demo |

**Note**: `COMMUNICATION/PROJECT_STATE.md` redirects to `state/project_state.md` (single source of truth).

---

### 6. Agent Memories and Learnings

**Purpose**: Preserve shared knowledge and patterns discovered during work

| Resource | Description | Owner |
|---|---|---|
| [state/meta_metrics.md](state/meta_metrics.md) | Convergence metrics (requirement churn, rework ratio, review cycles, demo validation time) | Meta-Optimizer Agent |
| [artifacts/meta/](artifacts/meta/) | Meta-layer artifacts (convergence audits, optimization proposals, workflow changes) | Meta-Optimizer Agent |
| [artifacts/debug/](artifacts/debug/) | Debug intelligence artifacts (root cause summaries, observability improvements) | Debug Intelligence Agent |

**Planned** (not yet implemented):
- Agent memory persistence (pattern recognition, recurring issues)
- Shared learnings catalog

---

### 7. Development and Coding Rules

**Purpose**: Maintain consistency and quality

| Resource | Description | Scope |
|---|---|---|
| [AI_ROLES.md](AI_ROLES.md) § Mutual Verification Protocol | Verification and handoff rules | All agents |
| [AGENTS.md](AGENTS.md) § Protocollo di handover | Task handover workflow | All agents |
| [.ecosystem/rules/](. ecosystem/) | Veto gates, HRA protocol, artifact handoff protocol | All agents |
| ADR-0002 (Technology Stack) | Technology constraints per device | Implementation Agent |

**Key Rules**:
- Interfaces before code (define contracts first)
- Integration first (avoid isolated silos)
- Continuous documentation (keep docs current)
- Mutual verification ("previous agent may have made mistakes")

---

### 8. Testing Knowledge

**Purpose**: Ensure quality and prevent regressions

| Resource | Description | Audience |
|---|---|---|
| [COMMUNICATION/VALIDATION_REPORT.md](COMMUNICATION/VALIDATION_REPORT.md) | Validation report template | QA / Verification Agent |
| Task-specific QA reports in `artifacts/features/*/qa_report.md` | Feature-specific validation | QA / Verification Agent |
| M1-T2-B validation gate | Example of mandatory validation checkpoint | All agents |

**Validation Protocol**:
1. Implementation Agent completes feature
2. QA Agent produces validation report (error handling, documentation, exit codes, integration tests)
3. Validation must pass before feature marked `COMPLETED`

---

### 9. Debug Knowledge

**Purpose**: Diagnose failures and improve observability

| Resource | Description | Owner |
|---|---|---|
| [artifacts/debug/root_cause_summary.md](artifacts/debug/README.md) | Root cause analysis template | Debug Intelligence Agent |
| [VSCODE_DEBUGGING_GUIDE.md](VSCODE_DEBUGGING_GUIDE.md) | VS Code debugging setup | Implementation Agent |
| Debug Intelligence deliverables in `artifacts/debug/` | Observability improvements, debug audits | Debug Intelligence Agent |

**Core Question**: Can the human understand the failure within minutes?

---

### 10. Documentation and Communication

**Purpose**: Maintain documentation and coordinate agents

| Resource | Description | Owner |
|---|---|---|
| [COMMUNICATION/](COMMUNICATION/) | Multi-agent coordination files (task queue, implementation log, status updates) | All agents |
| [COMMUNICATION/TEMPLATES/](COMMUNICATION/TEMPLATES/) | Task and status templates | All agents |
| [QUICK_REFERENCE.md](QUICK_REFERENCE.md) | Quick reference card | All agents |

**Documentation Agent responsibilities**:
- Maintain technical docs
- Detect inconsistencies
- Improve human readability
- **Read before writing** (never rewrite everything unnecessarily)

---

### 11. Capabilities (Reusable Know-How)

**Purpose**: Extract and catalog reusable procedures to reduce repeated work

| Resource | Description | Status |
|---|---|---|
| **[capabilities/](capabilities/)** | **Capabilities registry** | **PLANNED** (to be created) |

**Discovered Capabilities** (not yet formalized):
- MQTT topic structure validation
- CBOR serialization workflow
- Rust crate creation with `no_std` support
- PlantUML architecture diagram generation
- GitHub Pages documentation deployment
- Multi-agent handoff protocol

**Owner**: Librarian Agent (responsible for extraction and maintenance)

**Priority**: HIGH (critical for reducing token consumption and repeated work)

---

### 12. Reusable Patterns

**Purpose**: Document recurring solutions and architectural patterns

| Resource | Description | Status |
|---|---|---|
| Demo-Driven Development (DDD) pattern | Every feature requires Code + Docs + Observable Demo | ACTIVE (implicit) |
| Artifact-Based Handoff pattern | Use `artifacts/features/` for cross-role exchanges | ACTIVE |
| Validation Gate pattern | Mandatory validation checkpoint before unblocking dependencies | ACTIVE (M1-T2-B example) |

**Planned**: Extract and formalize additional patterns discovered during development.

---

### 13. Operational Procedures

**Purpose**: Document step-by-step procedures for common operations

| Resource | Description | Status |
|---|---|---|
| [ARCHITECTURE_WORKFLOW.md](ARCHITECTURE_WORKFLOW.md) | PlantUML → HTML documentation generation | DOCUMENTED |
| MQTT validation procedure | PC-to-RPi connectivity testing | IMPLICIT (to be extracted) |
| Rust crate creation procedure | Multi-target crate setup (std + no_std + WASM) | IMPLICIT (to be extracted) |
| Git commit procedure | Bash tool usage with safety protocol | DOCUMENTED (in Claude Code instructions) |

**Owner**: Librarian Agent (responsible for extraction and documentation)

**Priority**: MEDIUM (after capabilities registry)

---

## Meta-Knowledge: How to Use This Knowledge Base

### For Agents Starting a Task

1. **Read [DASHBOARD.md](DASHBOARD.md)** to understand current project state
2. **Check [TASK_QUEUE.md](COMMUNICATION/TASK_QUEUE.md)** for your assigned task
3. **Read relevant specs** from [specs/](specs/) and [protocols/](protocols/)
4. **Check [ADRs](adr/)** for architectural context
5. **Update [COMMUNICATION/TASKS/current_task.md](COMMUNICATION/TASKS/)** with `IN_PROGRESS` status

### For Agents Completing a Task

1. **Update [COMMUNICATION/IMPLEMENTATION_LOG.md](COMMUNICATION/)** with what was done
2. **Request validation** from QA Agent (produce `VALIDATION_REPORT.md`)
3. **Update [state/project_state.md](state/project_state.md)** after validation passes
4. **Extract capabilities** if reusable procedures were discovered (notify Librarian Agent)

### For Agents After Long Inactivity

1. **Read [DASHBOARD.md](DASHBOARD.md)** first (target: <5 min understanding)
2. **Scan [state/project_state.md](state/project_state.md)** for changes
3. **Check [TASK_QUEUE.md](COMMUNICATION/TASK_QUEUE.md)** for new priorities
4. **Review [state/meta_metrics.md](state/meta_metrics.md)** for ecosystem health

### For Librarian Agent Maintaining This Knowledge Base

1. **Detect duplication** — Same concept in multiple documents
2. **Consolidate knowledge** — Single source of truth for each concept
3. **Create cross-references** — Link related documents
4. **Extract capabilities** — Formalize reusable procedures
5. **Update this index** — Keep it current as new knowledge emerges

---

## Knowledge Base Evolution Log

**2026-07-11**: Knowledge Base created by Librarian Agent (architectural migration audit)  
- Initial index structure defined
- 13 knowledge categories catalogued
- Identified gaps: Capabilities registry, operational procedures, agent memories
- Priority: Create capabilities registry and dashboard

---

## Quick Links Summary

| Need | Resource |
|---|---|
| **Rapid re-entry after inactivity** | [DASHBOARD.md](DASHBOARD.md) |
| **Current work** | [TASK_QUEUE.md](COMMUNICATION/TASK_QUEUE.md) |
| **Project status** | [state/project_state.md](state/project_state.md) |
| **Architecture principles** | [README.md](README.md) |
| **My role and responsibilities** | [AI_ROLES.md](AI_ROLES.md), [AGENTS.md](AGENTS.md) |
| **Technical specs** | [specs/](specs/), [protocols/](protocols/) |
| **Decisions and rationale** | [adr/](adr/), [.ecosystem/DECISIONS.md](.ecosystem/DECISIONS.md) |
| **Templates for artifacts** | [COMMUNICATION/TEMPLATES/](COMMUNICATION/TEMPLATES/) |
| **Capabilities (reusable procedures)** | [capabilities/](capabilities/) (to be created) |
| **Ecosystem health metrics** | [state/meta_metrics.md](state/meta_metrics.md) |

---

**Maintained by**: Librarian Agent  
**Contact**: Claude Code / Antigravity  
**Improvement Suggestions**: Report to Meta-Optimizer Agent or create issue in `.ecosystem/`

