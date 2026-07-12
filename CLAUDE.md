# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

`tr4d3rz-docs` is the **Single Source of Truth** for the entire TR4D3RZ distributed evolutionary signal ecology system. This is a documentation-only repository owned by **Manus (Chief Architect)** that contains:

- ArchiMate 3.2 architecture diagrams (PlantUML format)
- Architectural Decision Records (ADRs)
- Protocol definitions and data contracts
- Technical specifications for all TR4D3RZ components
- Multi-agent workflow coordination rules

This repository generates a static HTML documentation site hosted at [https://simpego81.github.io/tr4d3rz-docs/](https://simpego81.github.io/tr4d3rz-docs/).

## Multi-Agent Ecosystem

TR4D3RZ is developed by a coordinated team of AI agents, each owning specific repositories:

| Repository | Scope | AI Owner |
|---|---|---|
| `tr4d3rz-docs` | Architecture, specs, ADRs (THIS REPO) | Manus |
| `tr4d3rz-core` | L-System genome, FSM runtime | Claude Code |
| `tr4d3rz-messaging` | MQTT/NATS, Gateway Nodes | Claude Code |
| `tr4d3rz-evolution` | Mutation, fitness, niche discovery | Claude Code |
| `tr4d3rz-observatory` | UI, visualization, replay system | Antigravity |
| `tr4d3rz-persistence` | Event sourcing, archetype memory | Claude Code |
| `tr4d3rz-embedded` | ESP8266, STM32 optimization nodes | GitHub Copilot |

**Meta-Layer Agents** (operate orthogonally to feature development):
- **Meta-Optimizer Agent** (Claude Code): System optimization, convergence analysis, workflow improvement
- **Debug Intelligence Agent** (Claude Code): Root cause analysis, observability optimization, failure diagnosis

## Building the Documentation Site

The site is built from PlantUML source files and rendered as interactive HTML with SVG relationship arrows.

**Regenerate the entire documentation site:**
```powershell
powershell.exe -NoProfile -File .\generate_docs.ps1
```

**Preview the site:**
Open `docs/index.html` in a browser.

## Architecture Documentation Workflow

**CRITICAL:** When updating architecture, follow this exact sequence:

1. **Edit PlantUML source files** (`.puml` files in the root directory):
   - `device_*.puml` files define per-device architectures
   - `archimate_diagram_v2.puml` is the master diagram
   
2. **Update the knowledge base** (if adding new elements):
   - Descriptions and technical details are embedded in the HTML files
   - If you add new ArchiMate elements, you must update the `KB` (knowledge base) object in the corresponding HTML file

3. **Run the generator** to rebuild `docs/` folder (see command above)
   - This automatically regenerates:
     - All `docs/*.html` device pages
     - `docs/archimate_data.json` for the holistic view
     - Holistic view data feed is now synchronized with PUML changes

4. **Commit both** the `.puml` source files AND the generated `docs/` folder:
   - GitHub Pages automatically redeploys when `docs/` changes are pushed

**DO NOT edit HTML files directly** — they are auto-generated and will be overwritten.

**NEW**: The holistic view (`docs/holistic_view.html`) now automatically reflects PUML changes via `archimate_data.json`.

See `ARCHITECTURE_WORKFLOW.md` for detailed documentation on the generation system.

## ArchiMate Grid Structure

The interactive documentation site organizes elements into a strict 4x4 grid per ArchiMate 3.2 specification:

- **Rows (Layers):** Motivation, Business, Application, Technology
- **Columns (Aspects):** Active Structure, Behavior, Passive Structure, Motivation

Each element is clickable and displays: Type, Role in TR4D3RZ, Technology details, and Relationships.

## Directory Structure

```
tr4d3rz-docs/
├── README.md                  # Project overview and repository map
├── AI_AGENT_DOCUMENTATION.md  # Instructions for AI agents
├── ANTIGRAVITY.md             # Specific guidance for Antigravity
├── CLAUDE.md                  # This file
├── generate_docs.ps1          # PowerShell script to regenerate docs
├── device_*.puml              # Per-device ArchiMate diagrams (14 devices)
├── archimate_diagram_v2.puml  # Master ArchiMate diagram
├── specs/                     # Technical specifications by component
│   ├── core/
│   ├── messaging/
│   ├── evolution/
│   ├── observatory/
│   ├── persistence/
│   └── embedded/
├── adr/                       # Architectural Decision Records
├── diagrams/                  # Additional architecture diagrams
│   └── per-device/
├── protocols/                 # Protocol definitions and data contracts
│   └── mqtt-topic-structure.md
├── milestones/                # Milestone plans and tracking
└── docs/                      # Generated HTML site (committed to git)
    ├── index.html             # Homepage with device grid
    └── [device].html          # Per-device interactive pages
```

## Architectural Principles (Enforce These)

When creating or reviewing specifications, enforce these core principles:

1. **Interfaces Before Code**: All data contracts (CBOR schemas), MQTT topic structures, and component interfaces MUST be defined in `protocols/` or `specs/` before any implementation begins in other repositories.

2. **Open-Ended Evolution**: Avoid rigid structural limits in genome designs; use evolutionary pressure (fitness evaluation) instead of artificial constraints.

3. **Asynchronous Distributed Ecology**: No global synchronization. Nodes are delay-tolerant and communicate via asynchronous signaling (MQTT).

4. **Emergent Specialization**: Agents should dominate predictive niches, not aim for universal strategies.

5. **Distributed Observability**: Every significant event (birth, death, mutation, cooperative signal) must be serializable, replayable, and visualizable in the Observatory.

## Protocol Definitions

All inter-repository contracts are versioned and documented in `protocols/`:

- **MQTT Topic Structure**: `protocols/mqtt-topic-structure.md`
- All MQTT payloads use **CBOR encoding** unless specified otherwise
- QoS levels are defined per topic pattern (see mqtt-topic-structure.md)

**CRITICAL RULE**: No repository may change a shared protocol/contract without updating `tr4d3rz-docs/protocols/` first.

## Technology Stack Reference

When writing specifications, respect these technology constraints (from ADR-0002):

- **Core Runtime**: Rust (for core, messaging, evolution, persistence)
- **Browser Runtime**: WebAssembly (Rust → WASM compilation)
- **Visualization**: Three.js / WebGL
- **Embedded Serialization**: CBOR (compact binary format)
- **Messaging**: MQTT (primary), NATS (alternative for high-throughput scenarios)
- **Storage**: SQLite (local persistence), Parquet (large datasets)
- **Observatory**: TypeScript, WASM, Three.js

## Hardware Constraints

The system runs on heterogeneous hardware — always check device-specific constraints:

- **ESP8266**: 80MHz, 80KB RAM — extremely constrained
- **STM32F1/F3**: ARM Cortex-M3/M4 — no heap allocator
- **Raspberry Pi 2**: ARMv7, central MVP node for NanoMQ, scraper/relay and SQLite persistence services
- **Linux/Android/Browser**: Full-featured environments

**Before specifying a component**: Check the corresponding `device_*.puml` file to understand runtime and technology constraints for that device.

## Milestone Roadmap

- **M0 (Foundations)**: GitHub setup, architecture docs, protocol specs, multi-agent workflow ✅ Current
- **M1 (Foundational Backbone Single RPi2)**: MQTT messaging, minimal FSM runtime, OHLCV feed, ESP8266/simulator integration, persistence logger and minimal Observatory
- **M2 (Basic Evolution)**: Mutations, fitness evaluation, lineage tracking, replay system
- **M3 (Cooperative Ecology)**: Cooperative signaling, niche detection, archetype memory
- **M4 (Full Observatory)**: Galaxy visualization, full replay, topology analysis
- **M5 (Production)**: Ensemble confidence scoring, validation pipeline

## Writing ADRs

When creating new ADRs in `adr/`:

- Use the naming convention: `ADR-NNNN-short-title.md`
- Include: Date, Status (Draft/Accepted/Superseded), Author
- Structure: Context, Decision, Consequences, Mitigation (if negative consequences exist)
- ADRs are immutable once Accepted — create a new ADR to supersede, don't edit the original

## Writing Specifications

When creating specs in `specs/[component]/`:

- Define interfaces and contracts first (data structures, CBOR schemas, MQTT topics)
- Include version numbers for all protocols
- Document open questions explicitly (don't leave them implicit)
- Link to relevant ADRs for context on architectural decisions
- Specifications should be implementation-agnostic — avoid language-specific details

## Git Workflow

- **Main branch**: All work happens on `main`
- **Commit discipline**: Commit `.puml` changes together with generated `docs/` folder
- **GitHub Pages**: Automatically deploys from `docs/` folder on push to main

## Cross-Repository Coordination

When changes in `tr4d3rz-docs` affect other repositories:

1. Update protocol/spec in this repo first
2. Create a git commit with clear description of the contract change
3. Reference this commit hash when coordinating with other AI agents
4. Other repositories should not implement changes until the contract is merged in `tr4d3rz-docs`

This ensures `tr4d3rz-docs` remains the authoritative source of truth.
