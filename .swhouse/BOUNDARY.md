# Memory Boundary — TR4D3RZ instance

This file defines what goes in `.swhouse/` vs the existing TR4D3RZ state files. Both coexist (Option A, decided 2026-07-25).

## What goes in `.swhouse/memory/`

Use `.swhouse/memory/` for **organizational-level knowledge** produced by Software House AI 12-step cycles:

| Type | Examples | Location |
|------|----------|----------|
| Architectural decisions | "Adopt CBOR for all MQTT payloads", "MQTT QoS 1 for telemetry topics" | `memory/decisions/` |
| Cross-repo patterns | "Event sourcing pattern for distributed state", "Heartbeat probe pattern" | `memory/patterns/` |
| Architectural errors | "Synchronous MQTT call caused deadlock in gateway — root cause + lesson" | `memory/errors/` |
| Domain knowledge | "RPi2 ARMv7 memory constraints", "ESP8266 80KB RAM — allocation strategies" | `memory/knowledge/` |

## What stays in TR4D3RZ state files

| File | Content | Owner |
|------|---------|-------|
| `COMMUNICATION/IMPLEMENTATION_LOG.md` | Per-task implementation history with commit hashes | Developer subagent |
| `COMMUNICATION/TASK_QUEUE.md` | Active M1 tasks, dependencies, status | Orchestrator |
| `COMMUNICATION/TASKS/current_task.md` | Current task details | Developer / Orchestrator |
| `DASHBOARD.md` | Session re-entry snapshot | Orchestrator |
| `state/meta_metrics.md` | Implementation quality metrics (churn, rework, velocity) | PQM / Meta-Optimizer |
| `artifacts/meta/pqm_audit_*.md` | PQM audit reports | PQM |

## Rule of thumb

If the knowledge would be useful when designing a **new project** from scratch (a new TR4D3RZ-like system), it belongs in `.swhouse/`.

If the knowledge is only useful for understanding the **current implementation state** of this specific project, it stays in TR4D3RZ state files.
