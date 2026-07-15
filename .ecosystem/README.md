# .ecosystem — Decisioni operative e infrastruttura coordinamento

**Creato**: 2026-07-10  
**Aggiornato**: 2026-07-15 — semplificazione a single primary agent  
**Location**: `tr4d3rz-docs/.ecosystem/` (versionato con SSOT)

---

## Contenuto attuale

| File | Stato | Descrizione |
|---|---|---|
| `DECISIONS.md` | ACTIVE | Log delle decisioni operative con rationale |
| `README.md` | ACTIVE | Questo file |

---

## Note

Con la migrazione al modello single primary agent (2026-07-15), le strutture di coordinamento multi-agente (cognitive boards, veto gates, HRA protocol, artifact handoff protocol) non sono più necessarie nella forma originale.

Il coordinamento avviene ora tramite:
- `AGENTS.md` — ruoli, responsabilità, protocollo subagent
- `SUBAGENT_PROTOCOL.md` — orchestrazione subagent interni
- `COMMUNICATION/TASK_QUEUE.md` — task attivi e dipendenze
- `DASHBOARD.md` — stato globale e session resumption

Le decisioni operative continuano a essere registrate in `DECISIONS.md`.
