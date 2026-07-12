# TR4D3RZ — PROJECT_STATE

**Maintainer**: Manus / Antigravity  
**Last update**: 2026-06-14 (M1-T2-B avviato)  
**Current milestone**: M1 — Foundational Backbone  
**Architecture baseline**: Single Raspberry Pi 1/2 backbone (Mosquitto/NanoMQ)

---

## 1. Stato sintetico

| Area | Stato | Nota |
|---|---|---|
| Repository GitHub | READY | Repository inizializzati e mappati. |
| Single RPi restructuring | DONE | Topologia allineata a RPi1/RPi2. |
| Contratti MVP | READY | `MVP_INTERFACE_CONTRACTS.md` definisce schemi v0.1. |
| Multi-agent workflow | ACTIVE | Protocollo Markdown-driven operativo. |
| Implementazione codice | IN PROGRESS | M1-T1 e M1-T2 (Rust Lib) completati. |

---

## 2. Blocchi e decisioni

| ID | Decisione | Esito |
|---|---|---|
| D-M1-001 | Usare 7 repository | Applicato. |
| D-M1-002 | RPi come nodo unico per broker/persistence | Applicato. |
| D-M1-003 | CBOR per capsule/fitness | Applicato. |
| D-M1-004 | Downgrade a RPi 1 Model B + Mosquitto | Applicato per limitazioni hardware rilevate (Claude Code). |
| D-M1-005 | Validazione Automatica Remota | **ACCETTATA**: M1-T2-B assegnato a Claude Code. Validation gate obbligatorio prima di M1-T5. |

---

## 3. Prossimo passo operativo

M1-T2-B è IN_PROGRESS. Claude Code deve implementare `remote_validation_probe.rs` in `tr4d3rz-messaging/examples/` seguendo la specifica in `COMMUNICATION/TASKS/M1-T2-B-MQTT-VALIDATION-SPEC.md` e il task file in `COMMUNICATION/TASKS/M1-T2-B-TASK-CLAUDE.md`. GitHub Copilot validerà il tool al completamento. M1-T5 rimane BLOCKED fino a M1-T2-B COMPLETED.

