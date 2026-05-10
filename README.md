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
| `tr4d3rz-observatory` | Ecosystem Observatory UI, Replay System | TypeScript, WASM, Three.js | Gemini CLI |
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
└── milestones/                # Milestone plans and tracking
```
