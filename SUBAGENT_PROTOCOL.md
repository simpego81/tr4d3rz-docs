# SUBAGENT_PROTOCOL.md — TR4D3RZ Subagent Orchestration Protocol

> **Owner**: Claude Code (Orchestratore)  
> **Aggiornato**: 2026-07-16 — migrazione a Option C (10 tipi specializzati)  
> **Scopo**: Definisce come l'Orchestratore spawna e gestisce i subagent specializzati.  
> **Riferimento ruoli**: `agents/` (source of truth per trigger, brief, output schema di ogni ruolo)

---

## 1. Principi base

1. **Autocontenimento**: ogni brief include tutto il contesto — il subagent non vede la conversazione corrente
2. **Single responsibility**: ogni subagent esegue un compito preciso e restituisce JSON strutturato
3. **Verifica degli output**: l'Orchestratore valida i risultati prima di procedere
4. **Parallelismo sicuro**: task implementativi paralleli usano worktree isolati
5. **Fallback esplicito**: output null o blockers → gestione esplicita prima di procedere
6. **Ruolo-prima-del-brief**: l'Orchestratore legge `agents/<role>.md` prima di costruire ogni brief

---

## 2. Taxonomy dei subagent (Option C — 10 tipi)

| Tipo | Agent tool type | Trigger principale | Worktree | File ruolo |
|---|---|---|---|---|
| **planner** | `Plan` | Spec incompleta o assente | No | [agents/planner.md](agents/planner.md) |
| **architect** | `claude` | ADR, nuovo protocollo, contratto cross-repo | No | [agents/architect.md](agents/architect.md) |
| **developer** | `claude` | Task IN_PROGRESS con spec completa | Sì (se parallelo) | [agents/developer.md](agents/developer.md) |
| **reviewer** | `code-reviewer` | Post-impl su task critico, o `review_recommended: true` | No | [agents/reviewer.md](agents/reviewer.md) |
| **debugger** | `claude` | Test failure, anomalia runtime, verdict FAIL | No | [agents/debugger.md](agents/debugger.md) |
| **tester** | `claude` | Pre-COMPLETED con integration test, pre-release | No | [agents/tester.md](agents/tester.md) |
| **documentation** | `claude` | OBBLIGATORIO post-developer che cambia stato sistema | No | [agents/documentation.md](agents/documentation.md) |
| **pqm** | `claude` | Ogni 3 task, session stale, soglie Meta-Optimizer | No | [agents/pqm.md](agents/pqm.md) |
| **pipeline-manager** | `claude` | Post-merge main (STUB — attivo post-M1) | No | [agents/pipeline-manager.md](agents/pipeline-manager.md) |
| **deployment-manager** | `claude` | Release tag, deploy esplicito (STUB — attivo post-M1) | No | [agents/deployment-manager.md](agents/deployment-manager.md) |

> **Research** (Explore type): non è un ruolo costituzionale ma rimane disponibile come utility per esplorazione codebase. Non ha file in `agents/` — usare direttamente con brief estemporaneo.

---

## 3. Flow di orchestrazione — task singolo

### Task con spec presente (caso più comune)

```
Orchestratore
  ├── [opzionale] research → comprende pattern esistenti
  ├── developer → implementa → aggiorna IMPLEMENTATION_LOG
  ├── [task critico] reviewer → PASS/FAIL/PARTIAL
  ├── [se FAIL] debugger → root cause → developer (fix) → tester
  └── documentation → sync state/ArchiMate [OBBLIGATORIO se componente cambiato]
```

### Task con spec assente (nuova feature)

```
Orchestratore
  ├── planner → crea spec in specs/<component>/
  ├── [se ADR necessario] architect → crea ADR → propone a owner
  ├── [attende approvazione owner se contratto modificato]
  ├── developer → implementa
  ├── reviewer (sempre su nuova feature)
  └── documentation [OBBLIGATORIO]
```

### Bug fix

```
Orchestratore
  ├── debugger → root cause + proposed fix
  ├── developer → implementa fix
  ├── tester → verifica fix
  └── documentation [se cambia stato componente]
```

---

## 4. Flow di orchestrazione — task paralleli

```
Orchestratore
  ├── Verifica indipendenza: i task non modificano gli stessi file
  └── pipeline(tasks, task => developer_subagent(task, isolation='worktree'))
         ├── task A → worktree A → implementa M1-T3
         ├── task B → worktree B → implementa M1-T4
         └── [dopo completamento] reviewer su entrambi + documentation
```

**Parallelizzare solo se**: i deliverable dei task non hanno file in comune.  
**Non parallelizzare se**: task B usa tipi o output prodotti da task A.

---

## 5. Come costruire un brief

Per ogni subagent, l'Orchestratore:

1. Legge `agents/<role>.md` → sezione "Mandatory Input"
2. Raccoglie i file elencati
3. Copia il "Brief Template" e sostituisce i `<PLACEHOLDER>`
4. Aggiunge il path del file di ruolo stesso nel brief

### Template base (da specializzare con il file di ruolo)

```
Sei il <ROLE> del team TR4D3RZ.

Leggi obbligatoriamente:
  - C:\projects\seq\tr4d3rz-docs\agents\<ROLE>.md  ← le tue regole operative
  - C:\projects\seq\tr4d3rz-docs\docs\CONSTITUTION.md  ← se necessario
  - <FILE_SPEC_1>
  - <FILE_SPEC_2>

Task / Obiettivo: <DESCRIPTION>

Deliverable: <LIST>

Restituisci il JSON di output definito in agents/<ROLE>.md.
```

> **Nota**: i brief template completi con tutti i placeholder sono nei file `agents/<role>.md`.

---

## 6. Gestione risultati subagent

```
risultato = subagent(brief)

if risultato == null:
    log("Subagent non ha restituito output. Gestire manualmente.")
    return BLOCKED

if risultato.status == "BLOCKED":
    if risultato.blockers sono architetturali:
        proponi_a_owner(risultato.blockers)
    else:
        risolvi_e_riprova()

if risultato.status == "PARTIAL":
    if retry_required == true:
        fix_inputs_and_retry()

if task_critico and risultato.status == "COMPLETED":
    verdict = reviewer_subagent(risultato.deliverables)
    if verdict.verdict == "FAIL":
        debugger_output = debugger_subagent(verdict.findings)
        developer_subagent(fix=debugger_output.proposed_fix)
        tester_subagent()

# Sempre, se il task ha cambiato stato componenti:
documentation_subagent()
```

---

## 7. Aggiornamento stato dopo ogni task

| File | Chi aggiorna | Quando |
|---|---|---|
| `<repo>/COMMUNICATION/TASKS/current_task.md` | Developer (nel DoD) | Fine implementazione |
| `<repo>/COMMUNICATION/IMPLEMENTATION_LOG.md` | Developer (nel DoD) | Fine implementazione |
| `tr4d3rz-docs/COMMUNICATION/TASK_QUEUE.md` | Orchestratore | Post-developer |
| `tr4d3rz-docs/state/project_state.md` | Documentation Agent | Post-developer |
| `tr4d3rz-docs/state/roadmap.yaml` | Documentation Agent | Post-developer |
| `tr4d3rz-docs/DASHBOARD.md` | Orchestratore | Fine sessione |
| `artifacts/meta/pqm_audit_*.md` | PQM | Post-audit |

---

## 8. Trigger PQM

L'Orchestratore spawna il PQM quando:
- Ogni 3 task completati nella sessione corrente (contatore)
- Session start se DASHBOARD stale > 2 giorni
- Meta-Optimizer threshold superata (AGENTS.md §8)
- Owner richiede esplicitamente

---

## 9. Session resumption — entry point

All'inizio di ogni sessione, l'Orchestratore legge nell'ordine:

1. `tr4d3rz-docs/docs/CONSTITUTION.md` — il contratto fondante
2. `tr4d3rz-docs/AGENTS.md` — modello agenti corrente
3. `tr4d3rz-docs/COMMUNICATION/TASK_QUEUE.md` — task attivi e dipendenze
4. `tr4d3rz-docs/COMMUNICATION/TASKS/current_task.md` — task in corso

Se DASHBOARD.md è stale (> 2 giorni): aggiornarlo è la prima azione.

---

## 10. Research (utility — non ruolo costituzionale)

Il subagent di tipo **research** (Explore) rimane disponibile per esplorazione codebase quando servono più di 3 query. Non ha file in `agents/`.

```
Read-only exploration del codebase TR4D3RZ.
Profondità: [quick | medium | very thorough]
Obiettivo: <domanda specifica>
Cerca in: <path o pattern>
Contesto: <perché serve questa info>

Restituisci: file trovati, definizioni rilevanti, pattern da riutilizzare.
```

---

*Maintainer: Claude Code (Orchestratore) — Aggiornato: 2026-07-16*
