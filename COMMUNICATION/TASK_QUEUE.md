# TR4D3RZ — TASK_QUEUE MVP Milestone 1

**Status**: Active  
**Owner**: Manus  
**Protocollo**: Markdown-driven handover in `COMMUNICATION/`  
**Milestone**: M1 — Foundational Backbone Single RPi2

---

## 1. Sequenza di esecuzione raccomandata

| ID | Repo | Agent | Stato | Dipendenze | Output richiesto |
|---|---|---|---|---|---|
| M1-T0 | `tr4d3rz-docs` | Manus | COMPLETED | Nessuna | `SPEC_MASTER.md`, `TASK_QUEUE.md`, contratti MVP, `project-tasks.md`. |
| M1-T1 | `tr4d3rz-core` | Claude Code | PENDING | M1-T0 | Tipi Rust condivisi: OHLCV, Genome Capsule, Fitness Result, trait FSM. |
| M1-T2 | `tr4d3rz-messaging` | Claude Code | PENDING | M1-T0, M1-T1 schema | NanoMQ RPi2, bridge topic, smoke publisher/subscriber, config systemd. |
| M1-T3 | `tr4d3rz-persistence` | Claude Code | PENDING | M1-T0, M1-T1 | Event logger SQLite, schema append-only, subscriber MQTT. |
| M1-T4 | `tr4d3rz-evolution` | Claude Code | PENDING | M1-T1, M1-T2 | CLI Linux che pubblica capsule MVP e ascolta fitness result. |
| M1-T5 | `tr4d3rz-embedded` | GitHub Copilot | PENDING | M1-T1, M1-T2 | Simulatore o firmware ESP8266 per capsule in/fitness out. |
| M1-T6 | `tr4d3rz-observatory` | Gemini CLI | PENDING | M1-T2, M1-T3 | UI browser con timeline eventi, stato nodi e fitness. |
| M1-T7 | Cross-repo | Gemini CLI | PENDING | M1-T1..M1-T6 | `ARCHITECTURAL_AUDIT.md` e `PROJECT_STATE.md` aggiornato. |

---

## 2. Regole di handover

Ogni agent deve leggere `SPEC_MASTER.md`, `protocols/MVP_INTERFACE_CONTRACTS.md` e il proprio task in `COMMUNICATION/TASKS/` prima di scrivere codice. Ogni task passa da `PENDING` a `IN_PROGRESS` prima dell'implementazione e a `COMPLETED` solo dopo test o validazione manuale documentata.

| Evento | File da aggiornare | Responsabile |
|---|---|---|
| Avvio task | `COMMUNICATION/TASKS/current_task.md` nel repo target | Agent assegnato. |
| Fine implementazione | `COMMUNICATION/IMPLEMENTATION_LOG.md` | Claude/Gemini/Copilot secondo ruolo. |
| Validazione | `COMMUNICATION/VALIDATION_REPORT.md` | GitHub Copilot o agent validator. |
| Audit | `COMMUNICATION/ARCHITECTURAL_AUDIT.md` | Gemini CLI. |
| Chiusura | `COMMUNICATION/PROJECT_STATE.md` e `docs/project-tasks.md` | Manus o Gemini dopo audit. |

---

## 3. Primo task da assegnare a Claude

Il primo task eseguibile è **M1-T2**, perché il protocollo operativo richiede esplicitamente l'implementazione del broker MQTT consolidato su RPi2. Tuttavia, M1-T2 deve importare o duplicare temporaneamente gli schemi v0.1 definiti in M1-T0 finché M1-T1 non produce il crate `tr4d3rz-core` stabile.

La consegna iniziale a Claude è disponibile in `COMMUNICATION/TASKS/current_task.md`.
