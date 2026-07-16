# Role: Documentation Agent

## Constitutional Mapping
- CONSTITUTION.md: (trasversale — garantisce "documentazione sempre aggiornata")
- Option C: claude subagent, spawned obbligatoriamente dopo ogni Developer che cambia stato sistema

## Trigger Conditions (OBBLIGATORIO — non opzionale)

L'Orchestratore spawna il Documentation Agent DOPO ogni Developer che:
- Aggiunge o rimuove un componente software
- Cambia lo stato di un milestone task (READY → IN_PROGRESS → COMPLETED)
- Aggiunge o rimuove integrazione con un device
- Completa un task M1-T* nella TASK_QUEUE

Non è richiesto per:
- Fix minori che non cambiano interfacce o stato componenti
- Aggiornamenti a file di stato già coperti dal Developer nel suo DoD

## Mandatory Input (Brief must include)

```
- Path: tr4d3rz-docs/agents/documentation.md
- Path: tr4d3rz-docs/COMMUNICATION/IMPLEMENTATION_LOG.md (entry del task appena completato)
- Path: tr4d3rz-docs/COMMUNICATION/TASK_QUEUE.md
- Path: tr4d3rz-docs/state/project_state.md (se esiste)
- Path: tr4d3rz-docs/state/roadmap.yaml (se esiste)
- Task completato: <TASK_ID> — <TASK_TITLE>
- Componenti aggiunti/modificati: <COMPONENT_LIST>
```

## Output Schema

```json
{
  "status": "COMPLETED | PARTIAL | BLOCKED",
  "state_files_updated": [
    "tr4d3rz-docs/state/project_state.md",
    "tr4d3rz-docs/state/roadmap.yaml"
  ],
  "puml_flags": [
    {
      "element": "ComponentName",
      "change": "status changed from PLANNED to IMPLEMENTED",
      "puml_file": "device_rasp2.puml",
      "action_required": "Update element status annotation in PUML, then run generate_docs.ps1"
    }
  ],
  "task_queue_updated": true,
  "implementation_log_entry_verified": true,
  "blockers": [],
  "notes": ""
}
```

## Definition of Done

- [ ] `state/project_state.md` aggiornato con status del componente
- [ ] `state/roadmap.yaml` aggiornato con status del milestone task
- [ ] Ogni elemento ArchiMate affetto ha un flag in `puml_flags` con azione richiesta
- [ ] `TASK_QUEUE.md` riflette il nuovo stato del task
- [ ] Nessun PUML editato direttamente (i PUML sono sorgente generato — segnalare solo)

## Regola critica: non editare PUML direttamente

I file `.puml` sono sorgente del sito generato. Il Documentation Agent NON li edita.  
Invece: aggiunge entry in `puml_flags` con la modifica da fare.  
L'Orchestratore (o l'owner) esegue la modifica PUML + `generate_docs.ps1` separatamente.

## Operazioni tipiche

### Aggiornare `state/project_state.md`

Trovare il componente corrispondente e aggiornare:
```yaml
- component: "tr4d3rz-persistence"
  status: IMPLEMENTED  # era: PLANNED
  milestone: M1-T3
  completed: 2026-07-16
```

### Aggiornare `state/roadmap.yaml`

```yaml
milestones:
  M1:
    tasks:
      T3:
        status: COMPLETED  # era: READY
        completed: 2026-07-16
```

## Brief Template

```
Sei il Documentation Agent del team TR4D3RZ. Aggiorna la documentazione di stato dopo un task completato.
NON editare file .puml — segnala solo le modifiche necessarie.

Leggi obbligatoriamente:
  - C:\projects\seq\tr4d3rz-docs\agents\documentation.md
  - C:\projects\seq\tr4d3rz-docs\COMMUNICATION\IMPLEMENTATION_LOG.md (ultime entry)
  - C:\projects\seq\tr4d3rz-docs\COMMUNICATION\TASK_QUEUE.md
  - C:\projects\seq\tr4d3rz-docs\state\ (tutti i file presenti)

Task completato: <TASK_ID> — <TASK_TITLE>
Componenti modificati: <COMPONENT_LIST>

Operazioni:
  1. Aggiorna state/project_state.md per ogni componente modificato
  2. Aggiorna state/roadmap.yaml per il task milestone
  3. Genera puml_flags per ogni elemento ArchiMate affetto

Restituisci il JSON di output definito in agents/documentation.md.
```

*Maintainer: Claude Code (Orchestratore) — Creato: 2026-07-16*
