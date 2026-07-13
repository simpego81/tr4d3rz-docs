# TR4D3RZ Capabilities Registry

**Purpose**: Catalog reusable know-how to reduce repeated work and token consumption  
**Maintainer**: Librarian Agent  
**Status**: ACTIVE  
**Created**: 2026-07-11

---

## What is a Capability?

A **capability** is reusable procedural knowledge — a documented workflow or pattern that solves a recurring problem. Capabilities are:

- **Executable procedures** — step-by-step instructions any agent can follow
- **Reusable** — applicable across multiple tasks or contexts
- **Tested** — proven to work through actual usage
- **Maintained** — kept current as technology or practices evolve

**Purpose**: Reduce token consumption by eliminating repeated discovery of the same procedures.

---

## Capability Catalog

| ID | Name | Category | Status | Last Used |
|---|---|---|---|---|
| CAP-001 | [MQTT Topic Validation](CAP-001-mqtt-topic-validation.md) | Messaging | PROPOSED | M1-T2 |
| CAP-002 | [CBOR Serialization Workflow](CAP-002-cbor-serialization.md) | Data | PROPOSED | M1-T1, M1-T2 |
| CAP-003 | [Rust Crate Creation (no_std + WASM)](CAP-003-rust-crate-nostd-wasm.md) | Development | **DOCUMENTED** | M1-T1, M1-T2 |
| CAP-004 | [PlantUML Architecture Diagram Generation](CAP-004-plantuml-generation.md) | Documentation | PROPOSED | M0 |
| CAP-005 | [GitHub Pages Documentation Deployment](CAP-005-github-pages-deployment.md) | Documentation | PROPOSED | M0 |
| CAP-006 | [Multi-Agent Artifact Handoff](CAP-006-artifact-handoff.md) | Workflow | **DOCUMENTED** | M1-T2-B |

**Total Capabilities**: 6 (2 documented, 4 proposed)  
**Categories**: Messaging (1), Data (1), Development (1), Documentation (2), Workflow (1)

---

## Capability Categories

### Messaging
Procedures related to MQTT, NATS, message protocols, topic structures, QoS levels.

### Data
Serialization, deserialization, data contracts, schema validation, CBOR/JSON/Parquet.

### Development
Rust crate creation, testing workflows, CI/CD patterns, cross-compilation.

### Documentation
Architecture diagrams, knowledge base maintenance, documentation generation.

### Workflow
Agent coordination, task handoff, validation gates, approval protocols.

### Testing
Test creation, validation procedures, integration testing, hardware validation.

### Embedded
ESP8266/STM32 firmware workflows, no_std patterns, memory optimization.

### Observatory
Visualization patterns, Three.js workflows, WASM integration, UI/UX patterns.

---

## How to Use a Capability

1. **Find the capability** — Browse catalog above or search by keyword
2. **Read the capability document** — Understand prerequisites, steps, and expected outcomes
3. **Follow the procedure** — Execute steps as documented
4. **Report issues** — Notify Librarian Agent if capability is outdated or incomplete
5. **Update usage** — Librarian Agent tracks capability reuse metrics

---

## How to Extract a New Capability

When you discover reusable procedural knowledge:

1. **Recognize the pattern** — "I'm doing something I (or another agent) might do again"
2. **Document it** — Use [TEMPLATE.md](TEMPLATE.md) to create capability document
3. **Notify Librarian Agent** — Request capability ID assignment
4. **Add to catalog** — Librarian Agent adds entry to this README
5. **Track reuse** — Meta-Optimizer Agent monitors capability reuse level

**Threshold for capability extraction**: If a procedure is used >1 time OR likely to be reused, extract it.

---

## Capability Template

See [TEMPLATE.md](TEMPLATE.md) for the standard capability document structure.

**Required sections**:
- Capability ID
- Name
- Category
- Purpose
- Prerequisites
- Procedure (step-by-step)
- Expected Outcomes
- Common Issues
- Last Updated

---

## Capability Metrics

**Tracked by Meta-Optimizer Agent in [state/meta_metrics.md](../state/meta_metrics.md)**:

| Metric | Definition | Target |
|---|---|---|
| **Capability Count** | Total capabilities extracted | Grow continuously |
| **Reuse Rate** | `capability_uses / total_tasks` | >0.3 (30% of tasks reuse capabilities) |
| **Token Savings** | Estimated tokens saved by reusing capabilities vs. re-discovering | Maximize |
| **Coverage** | % of task categories with at least one capability | >80% |

**Current Metrics** (baseline):
- Capability Count: 6
- Reuse Rate: TBD (track after M1 completion)
- Token Savings: TBD (requires usage tracking)
- Coverage: 50% (6/12 categories covered)

---

## Recent Capabilities

**2026-07-12**: First capabilities documented
- ✅ CAP-003 (Rust Crate no_std+WASM) — Fully documented from M1-T1, M1-T2
- ✅ CAP-006 (Multi-Agent Artifact Handoff) — Fully documented from M1-T2-B workflow
- 📝 CAP-001, CAP-002, CAP-004, CAP-005 remain in PROPOSED state

**2026-07-11**: Initial capability registry created
- CAP-001 to CAP-006 extracted from M0, M1-T1, M1-T2, M1-T2-B work
- Categories defined
- Template created

---

## Capability Lifecycle

```
DISCOVERED → PROPOSED → DOCUMENTED → ACTIVE → DEPRECATED
```

**DISCOVERED**: Pattern recognized but not yet documented  
**PROPOSED**: Capability document drafted, awaiting Librarian approval  
**DOCUMENTED**: Approved and added to catalog  
**ACTIVE**: Currently recommended for use  
**DEPRECATED**: Superseded by newer capability or no longer applicable

---

## Contact

**Maintainer**: Librarian Agent (Claude Code)  
**Report Issues**: Notify Librarian Agent or create entry in `.ecosystem/`  
**Request New Capability**: Notify Librarian Agent with procedure description

