# TR4D3RZ — Distributed Evolutionary Signal Ecology System

**Owner**: Manus (Chief Architect & Orchestrator)

This repository is the single source of truth for the entire TR4D3RZ project. It contains all architectural specifications, diagrams, decision records (ADRs), roadmaps, and cross-repository contracts.

---

## Project Vision

TR4D3RZ is a **distributed evolutionary research platform** — not a simple trading engine. It is a software biological ecosystem where agents evolve predictive FSM structures (genomes generated via L-System) on real OHLCV data from the Italian Stock Exchange (Borsa Italiana), cooperating via asynchronous signaling.

---

## Repository Map

| Repository | Role | Technology | AI Owner |
|---|---|---|---|
| `tr4d3rz-docs` | Architecture, specs, ADRs, roadmap | Markdown, D2 diagrams | Manus |
| `tr4d3rz-core` | L-System genome, FSM runtime, data contracts | Rust (WASM-compatible) | Claude Code |
| `tr4d3rz-messaging` | MQTT/NATS layer, Gateway Nodes | Rust / Python | Claude Code |
| `tr4d3rz-evolution` | Mutation, fitness, niche discovery | Rust / Python | Claude Code |
| `tr4d3rz-observatory` | Ecosystem Observatory UI, Replay System | TypeScript, WASM, Three.js | Claude Code |
| `tr4d3rz-persistence` | Archetype memory, event sourcing, lineage | Rust / Python | Claude Code |
| `tr4d3rz-embedded` | ESP8266, STM32 optimization nodes | C / C++ / Rust no_std | GitHub Copilot |

---

## Milestone Roadmap

| Milestone | Name | Key Deliverables |
|---|---|---|
| **M0** | Fondazioni | GitHub setup, architecture docs, protocol specs, multi-agent workflow |
| **M1** | MVP Distribuito | MQTT messaging, minimal FSM runtime, OHLCV simulator, ESP8266 integration, minimal Observatory |
| **M2** | Evoluzione Base | Mutations, fitness evaluation, lineage tracking, replay system |
| **M3** | Cooperative Ecology | Cooperative signaling, niche detection, archetype memory |
| **M4** | Full Observatory | Galaxy visualization, full replay, topology analysis |
| **M5** | Controlled Production Signals | Ensemble, confidence scoring, validation pipeline |

---

## Architectural Principles

1. **Open-Ended Evolution**: No rigid structural limits; use evolutionary pressure instead of artificial blocks.
2. **Asynchronous Distributed Ecology**: No global synchronization; delay-tolerant, opportunistically distributed.
3. **Emergent Specialization**: Agents dominate predictive niches, not universal strategies.
4. **Cooperative Signaling**: Agents cooperate via events/signals, never direct references.
5. **Distributed Observability**: Every important event is serializable, replayable, and visualizable.

---

## Multi-Agent Workflow Rules

1. **Interfaces Before Code**: Define contracts, protocols, and data structures before any implementation.
2. **Integration First**: Every milestone must integrate real components; avoid isolated silos.
3. **Continuous Documentation**: Every repository must maintain up-to-date architecture docs and diagrams.
4. **Repository Ownership**: Each repository has a defined AI owner responsible for its internal coherence.

---

## Directory Structure

```
tr4d3rz-docs/
├── README.md                  # This file
├── specs/                     # Technical specifications per component
│   ├── core/
│   ├── messaging/
│   ├── evolution/
│   ├── observatory/
│   ├── persistence/
│   └── embedded/
├── adr/                       # Architectural Decision Records
├── diagrams/                  # Architecture diagrams (D2/Mermaid)
├── protocols/                 # Protocol definitions and data contracts
├── milestones/                # Milestone plans and tracking
├── state/                     # Shared project state (project_state.md, meta_metrics.md)
├── artifacts/                 # Agent deliverables (features/, meta/, debug/)
└── COMMUNICATION/             # Multi-agent coordination and task tracking
```

---

## Documentation

- **[AI_ROLES.md](./AI_ROLES.md)** — Specialized role definitions for all agents
- **[AGENTS.md](./AGENTS.md)** — Agent responsibilities, repository ownership, and operational rules
- **[AI_AGENT_DOCUMENTATION.md](./AI_AGENT_DOCUMENTATION.md)** — Instructions for AI agents working on TR4D3RZ
- **[CLAUDE.md](./CLAUDE.md)** — Guidance for Claude Code when working in this repository
- **[ANTIGRAVITY.md](./ANTIGRAVITY.md)** — Guidance for Antigravity (Frontend/Observatory agent)
- **[META_LAYER_GUIDE.md](./META_LAYER_GUIDE.md)** — Meta-Optimizer and Debug Intelligence agents guide
- **[ARCHITECTURE_WORKFLOW.md](./ARCHITECTURE_WORKFLOW.md)** — Documentation generation workflow
- **[QUICK_REFERENCE.md](./QUICK_REFERENCE.md)** — Quick reference card for all agents

---

## Meta-Layer Agents

TR4D3RZ includes two meta-layer agents that operate orthogonally to feature development:

### Meta-Optimizer Agent (Claude Code)
**Purpose**: Optimize the AI ecosystem itself  
**Methods**: TRIZ, De Bono lateral thinking, systems thinking  
**Deliverables**: `artifacts/meta/`, `state/meta_metrics.md`

### Debug Intelligence Agent (Claude Code)
**Purpose**: Optimize human debugging experience  
**Scope**: All layers (frontend, backend, APIs, cloud, embedded, DB)  
**Deliverables**: `artifacts/debug/root_cause_summary.md`

See **[META_LAYER_GUIDE.md](./META_LAYER_GUIDE.md)** for details.

---

## Recent Updates

- **2026-06-19**: Gemini CLI roles migrated to Claude Code (Meta-Optimizer + Debug Intelligence agents)
- **2026-06-05**: M1-T2 and M1-T2-B completed
- **2026-05-23**: Initial repository setup
