# ADR-0001: Repository Structure

**Date**: 2026-05-10
**Status**: Accepted
**Author**: Manus (Chief Architect)

---

## Context

The TR4D3RZ system is a complex distributed ecosystem spanning multiple hardware targets (embedded MCUs, Linux PCs, Android devices, browsers), multiple technology stacks (Rust, C/C++, TypeScript, WASM), and multiple AI agents (Manus, Claude Code, Gemini CLI, GitHub Copilot). A clear repository structure is essential to maintain ownership, enable parallel development, and enforce interface-first discipline.

## Decision

The system is split into **7 repositories** under the `simpego81` GitHub account, each with a defined scope, technology stack, and AI owner:

| Repository | Scope | AI Owner |
|---|---|---|
| `tr4d3rz-docs` | Architecture, specs, ADRs | Manus |
| `tr4d3rz-core` | L-System, FSM runtime, data contracts | Claude Code |
| `tr4d3rz-messaging` | MQTT/NATS, Gateway Nodes | Claude Code |
| `tr4d3rz-evolution` | Mutation, fitness, niche discovery | Claude Code |
| `tr4d3rz-observatory` | UI, visualization, replay | Gemini CLI |
| `tr4d3rz-persistence` | Event sourcing, archetype memory | Claude Code |
| `tr4d3rz-embedded` | ESP8266, STM32 nodes | GitHub Copilot |

## Consequences

**Positive**: Clear ownership, parallel development possible, interfaces can be defined per-boundary, CI/CD can be configured per-repository.

**Negative**: Cross-repository changes require coordination; data contract changes in `tr4d3rz-core` must be propagated to all consumers.

## Mitigation

All inter-repository contracts (data schemas, event types, protocol definitions) are versioned and documented in `tr4d3rz-docs/protocols/`. No repository may change a shared contract without updating the docs repo first.
