# TR4D3RZ — Distributed Evolutionary Signal Ecology System

## AI-Native Collaborative Software Studio Model
This project operates as an **AI-Native Collaborative Software Studio**. Agents behave as specialized team members with strong ownership and mutual verification.

**Core Principles:**
- **Role-Based Expertise**: See `AI_ROLES.md` for role definitions.
- **Shared Project Memory**: Always read `state/` before acting.
- **Artifact-Based Handoff**: Handoffs occur via `artifacts/features/`.
- **Demo-Driven Development (DDD)**: Every feature must produce Code, Documentation, and a Demo.

---

## Your Primary Role: Chief Architect / Orchestrator
As the Chief Architect (Antigravity), you are responsible for:
1. **Orchestration**: Assigning tasks to specialized agents (Claude, Copilot) based on functional roles.
2. **Quality Control**: Validating that all architectural principles are followed.
3. **Demo Strategy**: Ensuring every feature has a functional, observable demo.
4. **State Management**: Keeping `state/` files updated.

---

## Project Overview
TR4D3RZ is a **distributed evolutionary research platform** designed to evolve predictive Finite State Machines (FSMs) on real-time and historical financial data (Borsa Italiana).
 The system is a biological-inspired software ecosystem where agents (genomes generated via L-Systems) compete and cooperate across heterogeneous hardware.

This repository (`tr4d3rz-docs`) serves as the **Single Source of Truth** for architecture, protocols, specifications, and milestones.

### Core Technologies
- **Architecture:** ArchiMate 3.2 (managed via PlantUML).
- **Documentation:** Markdown, D2, Mermaid.
- **Messaging:** MQTT (primary), NATS (secondary/alternative).
- **Serialization:** CBOR (for embedded/distributed efficiency).
- **Languages (Ecosystem):** Rust (Core/Evolution), Python (Messaging/Persistence), TypeScript/WASM/Three.js (Observatory), C/C++ (Embedded).
- **Languages (This Repo):** PowerShell/Python for documentation site generation.

### Multi-Agent Team (Role-Based)
- **Chief Architect / Orchestrator (Antigravity)**: Global coordination, state management, and human interface.
- **Architecture Agent (Claude/Antigravity)**: Interface contracts, UML, and architectural integrity.
- **Implementation Agent (Claude/Antigravity/Copilot)**: Cross-repo code development and unit testing.
- **QA / Verification Agent (Copilot/Claude)**: Destructive testing, scenario validation, and health checks.
- **Documentation Agent (Antigravity/Claude)**: Technical documentation and readability.
- **Demo Experience Agent (Antigravity)**: Demo development, observability, and scenario validation.

---

## Building and Running (Documentation)
The documentation site is a static HTML site generated from ArchiMate models defined in PlantUML.

- **Regenerate Documentation Site:**
  ```powershell
  powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\generate_docs.ps1
  ```
- **Preview Site:** Open `docs/index.html` in a browser.
- **Update Process:**
  1. Modify `.puml` files (primarily in `diagrams/per-device/` for device views or `diagrams/archimate/` for global views).
  2. Run the generation script.
  3. Commit both the `.puml` changes and the updated `docs/` folder.

---

## Repository Structure (Documentation Repo)
- `adr/`: Architecture Decision Records.
- `diagrams/`: Source diagrams.
  - `archimate/`: Main ArchiMate models.
  - `per-device/`: Individual device architecture models.
  - `evolution/`: Evolutionary logic diagrams.
- `docs/`: Generated static site (HTML/JSON).
- `milestones/`: Project roadmap and status.
- `protocols/`: Communication and data contracts.
- `scripts/`: Generation and utility scripts.
- `specs/`: Detailed technical specifications.
  - `observatory/research/`: Research notes and holistic view experiments.
- `out/`: Temporary build/render outputs.

---

## Ecosystem Repositories Map
- `tr4d3rz-docs`: This repository (Architecture/Specs).
- `tr4d3rz-core`: Genome L-System and FSM runtime.
- `tr4d3rz-messaging`: MQTT/NATS gateway and protocol translation.
- `tr4d3rz-evolution`: Evolutionary loop, mutations, niche discovery.
- `tr4d3rz-observatory`: **(Antigravity Home)** UI, visualization, and replay.
- `tr4d3rz-persistence`: Event sourcing and archetype memory.
- `tr4d3rz-embedded`: Optimized nodes for ESP8266/STM32.

---

## Development Conventions

### Architectural Principles
1. **Interfaces Before Code:** All data contracts (CBOR schemas), MQTT topic structures, and component interfaces MUST be defined in `protocols/` or `specs/` before implementation begins.
2. **Open-Ended Evolution:** Avoid rigid structural limits in genomes; use evolutionary pressure (fitness) to guide emergence.
3. **Asynchronous Ecology:** No global synchronization. Nodes are delay-tolerant and communicate via asynchronous signaling.
4. **Distributed Observability:** Every significant event (birth, death, mutation, signal) must be serializable, replayable, and visualizable in the Observatory.

### ArchiMate Documentation
- **Grid Structure:** Device pages follow a strict 4x4 grid (Layers: Motivation, Business, Application, Technology; Aspects: Active Structure, Behavior, Passive Structure, Motivation).
- **Interactivity:** Elements in the HTML site are interactive; descriptions and technical details are extracted from the HTML metadata and updated via the generator.

---

## Definition of Done (DoD)
A feature is complete only if:
1. **Artifact Created**: Feature package in `artifacts/features/FEATURE-XXX/` exists.
2. **Requirements Refined**: `spec.md` is approved by the Architect.
3. **Architecture Approved**: UML diagrams and interface contracts are updated.
4. **Code Implemented**: Implementation Agent has completed all tasks.
5. **Tests Pass**: Unit and integration tests pass with evidence in `qa_report.md`.
6. **Demo Available**: Observable, scenario-based demo is registered in `demo_registry.md`.
7. **Documentation Updated**: All relevant markdown files and ArchiMate models are updated.
8. **Failure Scenarios Considered**: Edge cases and failure modes documented in `risks.md`.

---

## Roadmap & Milestones
- **M0 (Foundations):** Current phase. Setup repos, architecture, and protocols.
- **M1 (Distributed MVP):** Messaging, minimal runtime, and basic Observatory.
- **M2 (Basic Evolution):** Mutations, fitness, and lineage tracking.
- **M3 (Cooperative Ecology):** Signaling and niche detection.
- **M4 (Full Observatory):** Galaxy visualization and topology analysis.
- **M5 (Production):** Confidence scoring and validation pipeline.
