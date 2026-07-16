# AGENTS.md — TR4D3RZ Agent Architecture (Option C)

> **Modello**: Orchestratore permanente (Claude Code) + subagent specializzati efimeri  
> **Riferimento costituzionale**: `docs/CONSTITUTION.md`  
> **Definizioni di ruolo**: `agents/` (source of truth per ogni ruolo)  
> **Ultimo aggiornamento**: 2026-07-16 — migrazione a Option C (Orchestratore + 10 subagent specializzati)

---

## 1. Gerarchia e actor model

```
User (Owner)
  ↕ approva: ADR, cambio protocolli, cambio priorità, rimozione componenti
  
Claude Code [ORCHESTRATORE — ruolo permanente]
  ├── Legge CONSTITUTION.md + TASK_QUEUE.md + current_task.md ad ogni sessione
  ├── Seleziona task → determina sequenza di fasi → spawna subagent
  ├── Integra output → aggiorna file di stato
  ├── Triggera PQM ogni 3 task o su soglia
  └── Propone all'owner per decisioni architetturali
  
Subagent specializzati [efimeri — spawned per fase]
  ├── Planner          [Plan-type]          — spec incomplete, nuova feature
  ├── Architect        [claude]             — ADR, protocollo, contratto nuovo
  ├── Developer        [claude + worktree]  — implementazione
  ├── Reviewer         [code-reviewer]      — QA avversariale post-impl.
  ├── Debugger         [claude]             — test failure, anomalia runtime
  ├── Tester           [claude]             — validazione pre-COMPLETED
  ├── Documentation    [claude]             — sync stato/ArchiMate (OBBLIGATORIO)
  ├── PQM              [claude]             — audit conformità Costituzione
  ├── Pipeline Mgr     [claude] STATUS:STUB — CI/CD GitHub Actions (post-M1)
  └── Deployment Mgr   [claude] STATUS:STUB — deploy device (post-M1)
```

**Regola fondamentale**: ogni ruolo ha la sua definizione completa in `agents/<role>.md`.  
L'Orchestratore legge il file di ruolo prima di costruire ogni brief.

---

## 2. Definizioni di ruolo

| File | Ruolo | Tipo subagent | Stato |
|---|---|---|---|
| [agents/orchestrator.md](agents/orchestrator.md) | Orchestratore | Claude Code primario | ACTIVE |
| [agents/planner.md](agents/planner.md) | Planner | Plan-type | ACTIVE |
| [agents/architect.md](agents/architect.md) | Architect | claude | ACTIVE |
| [agents/developer.md](agents/developer.md) | Developer | claude + worktree | ACTIVE |
| [agents/reviewer.md](agents/reviewer.md) | Reviewer | code-reviewer | ACTIVE |
| [agents/debugger.md](agents/debugger.md) | Debugger | claude | ACTIVE |
| [agents/tester.md](agents/tester.md) | Tester | claude | ACTIVE |
| [agents/documentation.md](agents/documentation.md) | Documentation Agent | claude | ACTIVE |
| [agents/pqm.md](agents/pqm.md) | Process Quality Manager | claude | ACTIVE |
| [agents/pipeline-manager.md](agents/pipeline-manager.md) | Pipeline Manager | claude | STUB |
| [agents/deployment-manager.md](agents/deployment-manager.md) | Deployment Manager | claude | STUB |

---

## 3. Repository di competenza

| Repository | Scope | Orchestratore può delegare? |
|---|---|---|
| `tr4d3rz-docs` | SSOT, architettura, spec, agents/, state/ | Sì — Documentation Agent e PQM |
| `tr4d3rz-core` | Tipi condivisi, FSM runtime | Sì — Developer + Reviewer |
| `tr4d3rz-messaging` | MQTT client, gateway | Sì — Developer + Reviewer |
| `tr4d3rz-evolution` | Mutazione, fitness, niche | Sì — Developer + Reviewer |
| `tr4d3rz-persistence` | Event sourcing, SQLite | Sì — Developer + Reviewer |
| `tr4d3rz-observatory` | UI, visualizzazione, replay | Sì — Developer + Reviewer |
| `tr4d3rz-embedded` | ESP8266, STM32 | Sì — Developer (no_std) |

**Regola protocolli**: nessun repo cambia un contratto condiviso senza aggiornare `protocols/` prima.

---

## 4. Sequenza di fasi per task type

| Tipo di task | Fasi obbligatorie | Fasi opzionali |
|---|---|---|
| Nuova feature (spec assente) | Planner → Architect → Developer → Documentation | Reviewer (se critico) |
| Implementazione (spec presente) | Developer → Documentation | Reviewer, Tester |
| Bug fix | Debugger → Developer → Tester → Documentation | Reviewer |
| ADR / protocollo | Architect | — |
| Validazione pre-release | Tester → PQM | — |
| Sync documentazione pura | Documentation | — |

---

## 5. Protocollo handover sessione

### Inizializzazione (ogni sessione)

Leggere in ordine:
1. `docs/CONSTITUTION.md`
2. `AGENTS.md` (questo file)
3. `COMMUNICATION/TASK_QUEUE.md`
4. `COMMUNICATION/TASKS/current_task.md`

Se DASHBOARD stale > 2 giorni: aggiornarlo prima di qualsiasi task.

### Fine task

1. `COMMUNICATION/TASKS/current_task.md` → COMPLETED
2. `COMMUNICATION/IMPLEMENTATION_LOG.md` → nuova entry
3. `COMMUNICATION/TASK_QUEUE.md` → status aggiornato
4. Spawna Documentation Agent se il task ha cambiato stato componenti

### Fine sessione

Aggiorna `DASHBOARD.md` con snapshot stato corrente.

---

## 6. Protocollo proposta → approvazione owner

**Attendere approvazione** per:
- Nuovi ADR (cambio architetturale)
- Modifica a `protocols/` (contratti condivisi)
- Cambio priorità tra milestone task
- Rimozione componenti esistenti
- Modifiche a `CONSTITUTION.md` o `AGENTS.md`

**Procedere autonomamente** per:
- Aggiornamenti file di stato (DASHBOARD, current_task, IMPLEMENTATION_LOG)
- Implementazione task già approvati in TASK_QUEUE
- Fix di inconsistenze documentazione
- Spawn subagent per task standard
- Scrittura file in `agents/` (nuovi ruoli → proporre; aggiornamenti di dettaglio → autonomo)

---

## 7. Gestione dei secret

- File `.env.test` con variabili sensibili sempre in `.gitignore`
- Nessun agente committe file `.env*`
- Convenzione variabili: `TR4D3RZ_<NOME>` in `.env.test` root del repo target

---

## 8. Meta-Optimizer — trigger di attivazione

L'Orchestratore si attiva in modalità Meta-Optimizer (proposta di miglioramento al PQM) quando rileva:

- Spec rivisitate >3 volte per la stessa feature
- Rework ratio >0.4 su un task (output PARTIAL + retry > 1 volta)
- Task COMPLETED senza git commit corrispondente
- Sessione che richiede >15 min per comprendere lo stato corrente
- PQM trova >3 findings HIGH in un singolo audit
- Owner richiede esplicitamente ottimizzazione

**Output**: `artifacts/meta/convergence_audit_<date>.md` + `artifacts/meta/optimization_proposals.md`

---

*Maintainer: Claude Code (Orchestratore) — Aggiornato: 2026-07-16*
