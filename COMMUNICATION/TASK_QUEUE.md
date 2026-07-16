# TR4D3RZ — TASK_QUEUE MVP Milestone 1

**Status**: Active  
**Owner**: User (approva decisioni architetturali) — Claude Code (Orchestratore)  
**Protocollo**: Markdown-driven handover in `COMMUNICATION/`  
**Milestone**: M1 — Foundational Backbone Single RPi2  
**Aggiornato**: 2026-07-16

---

## 1. Sequenza di esecuzione raccomandata

| ID | Repo | Agent | Stato | Dipendenze | Output richiesto |
|---|---|---|---|---|---|
| M1-T0 | `tr4d3rz-docs` | Manus | ✅ COMPLETED | Nessuna | `SPEC_MASTER.md`, `TASK_QUEUE.md`, contratti MVP, `project-tasks.md`. |
| M1-T1 | `tr4d3rz-core` | Claude Code | ✅ COMPLETED | M1-T0 | Tipi Rust condivisi: OHLCV, Genome Capsule, Fitness Result, trait FSM. |
| M1-T2 | `tr4d3rz-messaging` | Claude Code | ✅ COMPLETED (Rust lib) | M1-T0, M1-T1 | Rust MQTT client library. |
| M1-T2-B | `tr4d3rz-messaging` | Claude Code | ✅ COMPLETED | M1-T2 | Tool di validazione remota PC-to-RPi (Heartbeat Probe). **Validation gate obbligatorio prima di M1-T5.** |
| M1-T3 | `tr4d3rz-persistence` | Claude Code | 🔄 IN_PROGRESS (PARTIAL) | M1-T0, M1-T1, M1-T2 | Event logger SQLite, schema append-only, subscriber MQTT. Library parziale — manca: main.rs, config/, systemd/, migrations/ |
| M1-T4 | `tr4d3rz-evolution` | Claude Code | 🔲 READY | M1-T1, M1-T2 | CLI Linux che pubblica capsule MVP e ascolta fitness result. |
| M1-T5 | `tr4d3rz-embedded` | Claude Code | 🔲 READY | M1-T1, M1-T2, **M1-T2-B** | Simulatore o firmware ESP8266 per capsule in/fitness out. |
| M1-T6 | `tr4d3rz-observatory` | Claude Code | ⏸️ BLOCKED | M1-T2, M1-T3 | UI browser con timeline eventi, stato nodi e fitness. |
| M1-T7 | Cross-repo | Claude Code | ⏸️ BLOCKED | M1-T1..M1-T6 | `ARCHITECTURAL_AUDIT.md` e `PROJECT_STATE.md` aggiornato. |

### 1.1 Iniziative parallele

| ID | Repo | Agent | Stato | Dipendenze | Output richiesto |
|---|---|---|---|---|---|
| FEATURE-DOCS-PROJECT-MAP | `tr4d3rz-docs` | Claude Code | ✅ FUNCTIONALLY COMPLETE | — | Homepage Project Map, 4 mappe interattive, pagine dettaglio, pipeline CI/CD. Gate: browser validation PENDING_HUMAN. |
| FEATURE-VIEWS | `tr4d3rz-docs` | Claude Code | ✅ COMPLETED | — | 4 stakeholder views (stakeholders, process, roadmap, architecture). |
| **FEATURE-AGENT-ARCHITECTURE** | `tr4d3rz-docs` | Claude Code | 🔄 IN_PROGRESS (Fase 2) | Approvazione owner 2026-07-16 | Architettura agenti Option C: agents/ directory, AGENTS.md, SUBAGENT_PROTOCOL.md, state consistency, PQM audit. |

**FEATURE-AGENT-ARCHITECTURE — Fasi:**

| Fase | Status | Deliverable |
|---|---|---|
| Fase 1 — Fondazione | ✅ COMPLETED | agents/ (12 file), AGENTS.md, SUBAGENT_PROTOCOL.md aggiornati |
| Fase 2 — State Consistency | ✅ COMPLETED | IMPLEMENTATION_LOG repair, state inconsistencies fix, TASK_QUEUE update, DASHBOARD update, primo PQM audit |
| Fase 3 — DevOps | 🔲 PENDING (post-M1) | GitHub Actions CI, Pipeline Manager, Deployment Manager |

**FEATURE-DOCS-PROJECT-MAP task master**: `COMMUNICATION/TASKS/FEATURE-DOCS-PROJECT-MAP.md`

---

## 2. Regole di handover

Ogni agent deve leggere `SPEC_MASTER.md`, `protocols/MVP_INTERFACE_CONTRACTS.md` e il proprio task in `COMMUNICATION/TASKS/` prima di scrivere codice. Ogni task passa da `PENDING` a `IN_PROGRESS` prima dell'implementazione e a `COMPLETED` solo dopo test o validazione manuale documentata.

| Evento | File da aggiornare | Responsabile |
|---|---|---|
| Avvio task | `COMMUNICATION/TASKS/current_task.md` nel repo target | Agent assegnato. |
| Fine implementazione | `COMMUNICATION/IMPLEMENTATION_LOG.md` | Claude Code/Copilot secondo ruolo. |
| Validazione | `COMMUNICATION/VALIDATION_REPORT.md` | GitHub Copilot o agent validator. |
| Audit | `COMMUNICATION/ARCHITECTURAL_AUDIT.md` | Claude Code. |
| Chiusura | `COMMUNICATION/PROJECT_STATE.md` e `state/project_state.md` | Manus o Claude Code dopo audit. |

---

## 3. Stato attuale e prossimi passi

**Ultimo aggiornamento**: 2026-07-13

### Task Completati

✅ **M1-T0**: Specifiche, protocolli e contratti MVP (Manus)  
✅ **M1-T1**: `tr4d3rz-core` crate con tipi Rust condivisi (Claude Code)  
✅ **M1-T2**: `tr4d3rz-messaging` Rust MQTT library (Claude Code)

**Deliverable M1-T1**:
- Crate `tr4d3rz-core` v0.1.0
- Tipi: `OhlcvBar`, `OhlcvHistory`, `GenomeCapsule`, `FitnessResult`, `NodeStatus`
- Supporto `no_std` per embedded targets
- CBOR serialization
- 8/8 test passing
- Documentazione rustdoc completa

**Deliverable M1-T2 (Rust Library)**:
- Crate `tr4d3rz_messaging` v0.1.0
- MQTT client wrapper (rumqttc)
- Topic builder con validazione
- CBOR serialization automatica
- Publisher/Subscriber type-safe
- 12/13 test passing
- 3 esempi funzionanti
- Documentazione rustdoc completa
- CBOR size: 155B (FitnessResult), 192B (GenomeCapsule)

### Demo MVP Completata

✅ **MVP Browser Demo**: Demo browser-based validata con successo (Claude Code)

**Deliverable Demo**:
- Backend Node.js con MQTT broker (Aedes)
- 5 simulatori di nodi (Scraper, Evolution, ESP8266 x2, Logger)
- Frontend responsive con UI real-time
- Validazione flusso messaggi MQTT
- Conformità 100% ai contratti MVP v0.1

**Risultato**: Architettura M1 validata, pronta per implementazione reale.

### Prossimi Task (Ora Sbloccati)

🔲 **M1-T3**: `tr4d3rz-persistence` - Event sourcing e logging (Claude Code)

**Dipendenze soddisfatte**:
- ✅ M1-T0 (specifiche pronte)
- ✅ M1-T1 (tipi core pronti)
- ✅ M1-T2 (MQTT client disponibile)

**Requisiti**:
- Event logger SQLite con schema append-only
- MQTT subscriber per tutti gli eventi MVP
- Query API per Observatory
- Replay system MVP

🔲 **M1-T4**: `tr4d3rz-evolution` - Generazione e mutazione genomi (Claude Code)

**Dipendenze soddisfatte**:
- ✅ M1-T1 (tipi genome pronti)
- ✅ M1-T2 (MQTT client disponibile)

**Requisiti**:
- CLI Linux per generazione genomi
- Publisher capsule via MQTT
- Subscriber fitness results
- Mutation operator MVP

🔲 **M1-T5**: `tr4d3rz-embedded` - Simulatore o firmware ESP8266 (GitHub Copilot)

**Dipendenze soddisfatte**:
- ✅ M1-T1 (tipi core pronti)
- ✅ M1-T2 (MQTT client disponibile)
- ✅ M1-T2-B (heartbeat probe completato)

**Requisiti**:
- Firmware ESP8266 o simulatore
- Integrazione con broker MQTT per ricezione capsule
- Pubblicazione dei risultati di fitness

### Task Ancora Bloccati

⏸️ **M1-T6**: tr4d3rz-observatory (dipende da M1-T2, M1-T3)  
⏸️ **M1-T7**: Cross-repo audit (dipende da tutti i precedenti)
