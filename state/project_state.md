# TR4D3RZ — PROJECT_STATE

**Maintainer**: Claude Code (Orchestratore)  
**Last update**: 2026-07-16  
**Current status**: M1_IN_PROGRESS  
**Architecture baseline**: Single Raspberry Pi 2 backbone (NanoMQ/Mosquitto)

> Questo file è il SSOT per lo stato del progetto. `COMMUNICATION/PROJECT_STATE.md` è deprecato.

---

## 1. Executive Summary

| Area | Status | Note |
|---|---|---|
| Repositories | READY | 7 repository attivi su GitHub |
| Infrastructure | READY | Topologia Single RPi2 definita e validata (M1-T2-B) |
| MVP Contracts | READY | CBOR schemas e MQTT topics v0.1 stabili |
| Agent Model | OPTION_C | Orchestratore (Claude Code) + 10 subagent specializzati; AGENTS.md + agents/ aggiornati (2026-07-16) |
| Implementazione | IN PROGRESS | M1-T1, T2, T2-B completati; T3 IN_PROGRESS (PARTIAL); T4/T5 READY |
| FEATURE-DOCS-PROJECT-MAP | FUNCTIONALLY COMPLETE | Browser gate PENDING_HUMAN |
| ARCH-AGENTS | FASE_1_COMPLETE | agents/ directory (12 file), AGENTS.md, SUBAGENT_PROTOCOL.md aggiornati |

---

## 2. Stato Task M1

| Task | Status | Note |
|---|---|---|
| M1-T0 | COMPLETED | Spec, protocolli, contratti MVP |
| M1-T1 | COMPLETED | Tipi Rust condivisi; commit e8ecad4 su tr4d3rz-core |
| M1-T2 | COMPLETED | MQTT library Rust; commit af19bee su tr4d3rz-messaging |
| M1-T2-B | COMPLETED | Heartbeat Probe validato su RPi2 (2026-07-10) |
| M1-T3 | IN_PROGRESS (PARTIAL) | Library (event_logger.rs, schema.rs, lib.rs) esistente; manca main.rs, config/, systemd/, migrations/ |
| M1-T4 | PENDING | Repo tr4d3rz-evolution vuoto; dipendenze M1-T1/T2 soddisfatte |
| M1-T5 | PENDING | Simulatore/firmware ESP8266; gate M1-T2-B soddisfatto |
| M1-T6 | BLOCKED | Dipende da M1-T2 + M1-T3 |
| M1-T7 | BLOCKED | Dipende da tutti i task M1 |

---

## 3. Decisioni architetturali attive

| ID | Decisione | Esito |
|---|---|---|
| D-M1-001 | 7 repository separati | Applicato |
| D-M1-002 | RPi2 come nodo unico per broker/persistence | Applicato |
| D-M1-003 | CBOR per capsule/fitness | Applicato |
| D-M1-004 | Fallback a Mosquitto su RPi1 (dev profile) | Applicato; target resta NanoMQ su RPi2 |
| D-M1-005 | Heartbeat Probe come validation gate per M1-T5 | COMPLETED |
| D-2026-07-15 | Migrazione modello agenti: single primary (Claude Code) + subagent interni | Applicato (superato) |
| **D-2026-07-16** | **Architettura agenti Option C: Orchestratore + 10 subagent specializzati (agents/ directory)** | **Applicato** |

---

## 4. Ambiente

- **Master Node**: Raspberry Pi 2 Model B (IP: configurabile via `.env.test`)
- **Broker**: NanoMQ (porta 1883) o Mosquitto come fallback
- **Persistence**: SQLite (WAL mode)
- **Dev Env**: Windows 11 / WSL2 / VS Code
- **Agent Platform**: Claude Code + Agent tool (subagent interni)

---

## 5. Prossimi passi (priorità)

1. **Completare M1-T3** — main.rs subscriber MQTT, config, systemd, migrations
2. **Iniziare M1-T4** — Evolution CLI (dopo o in parallelo con T3 se deliverable indipendenti)
3. **Implementare M1-T5** — simulatore ESP8266
4. **Sbloccare M1-T6** — Observatory UI (dopo T3)

---

## 6. Rischi

| Rischio | Probabilità | Impatto | Mitigation |
|---|---|---|---|
| T3 parziale blocca T6 | MEDIO | ALTO | Completare binary subscriber |
| ESP8266 memory constraints | MEDIO | MEDIO | no_std, CBOR minimale |
| Observatory performance | BASSO | MEDIO | Deferred a M1-T6 |
| FEATURE-DOCS browser gate | BASSO | MEDIO | Richiede verifica manuale owner |

---

## 7. Prossimo audit

**Trigger** (audit immediato se):
- >5 task COMPLETED senza commit git corrispondente
- Requirement churn >3 per qualsiasi task
- Rework ratio >0.4
- Owner richiede audit

---

*SSOT per lo stato del progetto TR4D3RZ*  
*Ultimo aggiornamento: Claude Code (Orchestratore) — 2026-07-16*
