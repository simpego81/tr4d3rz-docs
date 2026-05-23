# TR4D3RZ — PROJECT_STATE

**Maintainer**: Manus  
**Last update**: 2026-05-23  
**Current milestone**: M1 — Foundational Backbone  
**Architecture baseline**: Single Raspberry Pi 2 backbone

---

## 1. Stato sintetico

| Area | Stato | Nota |
|---|---|---|
| Repository GitHub | READY | I repository indicati da ADR-0001 risultano esistenti nell'organizzazione/account `simpego81`. |
| Single RPi2 restructuring | DONE | Specifiche, diagrammi e HTML sono già stati allineati alla topologia Single RPi2. |
| Contratti MVP | READY FOR IMPLEMENTATION | `MVP_INTERFACE_CONTRACTS.md` definisce schemi v0.1 per capsule, fitness ed event log. |
| Multi-agent workflow | READY | `COMMUNICATION/` contiene task queue, master spec, template e current task. |
| Implementazione codice | NOT STARTED | In attesa di esecuzione task da Claude/Copilot/Gemini. |

---

## 2. Blocchi e decisioni

| ID | Decisione | Esito |
|---|---|---|
| D-M1-001 | Usare 7 repository invece dei “4” citati nelle istruzioni immediate | Applicato, perché ADR-0001 e M0 sono fonti autorevoli già accettate. |
| D-M1-002 | Mantenere RPi2 come nodo unico per broker, scraper, relay e persistence | Applicato, coerente con la restructuring Single RPi2. |
| D-M1-003 | Consentire payload JSON per OHLCV e CBOR per capsule/fitness | Applicato, coerente con ADR-0004 e con debug UI nell'MVP. |

---

## 3. Prossimo passo operativo

Il prossimo passo è consegnare a Claude Code `COMMUNICATION/TASKS/current_task.md` per avviare il backbone MQTT RPi2. Al completamento, Claude deve produrre `IMPLEMENTATION_LOG.md`; Copilot deve validare con smoke test MQTT; Gemini deve verificare coerenza cross-repo.
