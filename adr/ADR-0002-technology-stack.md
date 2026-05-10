# ADR-0002: Technology Stack

**Date**: 2026-05-10
**Status**: Accepted
**Author**: Manus (Chief Architect)

---

## Context

The system must run on hardware ranging from ESP8266 (80MHz, 80KB RAM) to modern Linux PCs and browsers. A coherent technology stack must be chosen that satisfies performance, portability, and safety requirements.

## Decisions

### Runtime Core: Rust

Rust is selected as the primary language for `tr4d3rz-core`, `tr4d3rz-messaging`, `tr4d3rz-evolution`, and `tr4d3rz-persistence`.

**Rationale**: Memory safety without GC, native performance, `no_std` support for embedded targets, and first-class WASM compilation target.

### Browser Runtime: WebAssembly

The FSM runtime from `tr4d3rz-core` will be compiled to WASM for execution in the browser Observatory.

**Rationale**: Enables running actual evolution logic in the browser without reimplementation, ensuring behavioral consistency.

### Visualization: Three.js / WebGL

The Observatory UI uses Three.js (or raw WebGL) for 3D visualizations (Evolution Galaxy, Signal Ecology).

**Rationale**: Required for rendering large numbers of agents in real-time with spatial clustering.

### Embedded Serialization: CBOR

CBOR is selected as the primary serialization format for embedded nodes.

**Rationale**: Compact binary format, well-supported in Rust and C, suitable for constrained environments. FlatBuffers is an alternative for zero-copy scenarios.

### Messaging: MQTT (primary), NATS (alternative)

MQTT is the primary messaging protocol for its lightweight nature and broad embedded support.

**Rationale**: MQTT is widely supported on ESP8266 and other constrained nodes. NATS is considered for higher-throughput scenarios between Linux nodes.

### Storage: SQLite (local), Parquet (large datasets)

**Rationale**: SQLite is universally available and suitable for Persistence Nodes (Raspberry Pi). Parquet is used for efficient columnar storage of large OHLCV datasets and lineage archives.

## Consequences

The choice of Rust as the primary language requires Claude Code as the primary implementer for core components. Gemini CLI handles TypeScript/JavaScript for the Observatory. GitHub Copilot assists with embedded C/C++ code.
