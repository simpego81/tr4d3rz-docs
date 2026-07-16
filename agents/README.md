# agents/ — TR4D3RZ Agent Role Definitions

Questa directory è la **source of truth** per tutti i ruoli agente nel sistema TR4D3RZ (Option C).  
Ogni file definisce un ruolo: trigger, input obbligatori, output atteso, DoD, brief template.

## Indice dei ruoli

| File | Ruolo Costituzionale | Tipo | Stato |
|---|---|---|---|
| [orchestrator.md](orchestrator.md) | Orchestratore | Claude Code primario | ACTIVE |
| [planner.md](planner.md) | Planner | Plan-type subagent | ACTIVE |
| [architect.md](architect.md) | Architect | claude subagent | ACTIVE |
| [developer.md](developer.md) | Developer | claude subagent + worktree | ACTIVE |
| [reviewer.md](reviewer.md) | Reviewer | code-reviewer subagent | ACTIVE |
| [debugger.md](debugger.md) | Debugger | claude subagent | ACTIVE |
| [tester.md](tester.md) | Tester | claude subagent | ACTIVE |
| [documentation.md](documentation.md) | Documentation Agent | claude subagent | ACTIVE |
| [pqm.md](pqm.md) | Process Quality Manager | claude subagent | ACTIVE |
| [pipeline-manager.md](pipeline-manager.md) | Pipeline Manager | claude subagent | STUB |
| [deployment-manager.md](deployment-manager.md) | Deployment Manager | claude subagent | STUB |

## Come usare questi file

**L'Orchestratore** (Claude Code primario) legge i file di ruolo per:
1. Decidere quale subagent spawnare dato il contesto del task
2. Costruire il brief con i parametri corretti
3. Validare l'output ricevuto contro lo schema atteso

**I subagent** ricevono il path del proprio file di ruolo nel brief e lo leggono come prima azione.

## Struttura di ogni file di ruolo

```
# Role: <Nome>
## Constitutional Mapping   — collegamento alla CONSTITUTION.md
## Trigger Conditions       — quando l'Orchestratore spawna questo agente
## Mandatory Input          — file e contesto obbligatori nel brief
## Output Schema            — JSON strutturato atteso
## Definition of Done       — checklist di completamento
## Brief Template           — testo da usare nell'invocazione Agent tool
```

## Aggiornamento

I file in `agents/` sono aggiornati dal **PQM** su proposta dell'Orchestratore.  
Ogni modifica richiede approvazione dell'owner se cambia il comportamento operativo di un ruolo.

*Maintainer: Claude Code (Orchestratore) — Creato: 2026-07-16*
