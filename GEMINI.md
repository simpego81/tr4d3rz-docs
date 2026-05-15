# TR4D3RZ — Distributed Evolutionary Signal Ecology System

## Project Overview
TR4D3RZ is a **distributed evolutionary research platform** designed to evolve predictive Finite State Machines (FSMs) on real-time and historical financial data (Borsa Italiana). The system is a biological-inspired software ecosystem where agents (genomes generated via L-Systems) compete and cooperate across heterogeneous hardware.

This repository (`tr4d3rz-docs`) serves as the **Single Source of Truth** for architecture, protocols, specifications, and milestones.

### Core Technologies
- **Architecture:** ArchiMate 3.2 (managed via PlantUML).
- **Documentation:** Markdown, D2, Mermaid.
- **Messaging:** MQTT (primary), NATS (secondary/alternative).
- **Serialization:** CBOR (for embedded/distributed efficiency).
- **Languages (Ecosystem):** Rust (Core/Evolution), Python (Messaging/Persistence), TypeScript/WASM/Three.js (Observatory), C/C++ (Embedded).
- **Languages (This Repo):** PowerShell/Python for documentation site generation.

### Multi-Agent Team
- **Manus (Chief Architect):** Orchestrator and owner of this repo.
- **Claude Code:** Backend, Core, Messaging, Evolution, Persistence.
- **Gemini CLI:** Observatory UI, Ecosystem Visualization, Replay System.
- **GitHub Copilot:** Embedded optimization nodes.

---

## Building and Running (Documentation)
The documentation site is a static HTML site generated from ArchiMate models defined in PlantUML.

- **Regenerate Documentation Site:**
  ```powershell
  powershell.exe -NoProfile -File .\generate_docs.ps1
  ```
- **Preview Site:** Open `docs/index.html` in a browser.
- **Update Process:**
  1. Modify `.puml` files (either in the root or `diagrams/per-device/`).
  2. Run the generation script.
  3. Commit both the `.puml` changes and the updated `docs/` folder.

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

### Repository Map
- `tr4d3rz-docs`: This repository (Architecture/Specs).
- `tr4d3rz-core`: Genome L-System and FSM runtime.
- `tr4d3rz-messaging`: MQTT/NATS gateway and protocol translation.
- `tr4d3rz-evolution`: Evolutionary loop, mutations, niche discovery.
- `tr4d3rz-observatory`: **(Gemini CLI Home)** UI, visualization, and replay.
- `tr4d3rz-persistence`: Event sourcing and archetype memory.
- `tr4d3rz-embedded`: Optimized nodes for ESP8266/STM32.

---

## Roadmap & Milestones
- **M0 (Foundations):** Current phase. Setup repos, architecture, and protocols.
- **M1 (Distributed MVP):** Messaging, minimal runtime, and basic Observatory.
- **M2 (Basic Evolution):** Mutations, fitness, and lineage tracking.
- **M3 (Cooperative Ecology):** Signaling and niche detection.
- **M4 (Full Observatory):** Galaxy visualization and topology analysis.
- **M5 (Production):** Confidence scoring and validation pipeline.
