# SUBAGENT_PROTOCOL.md — TR4D3RZ Subagent Orchestration Protocol

> **Owner**: Claude Code (Primary Agent)  
> **Creato**: 2026-07-15  
> **Scopo**: Definisce come Claude Code orchestra subagent interni per parallelismo e specializzazione. Letto da Claude Code all'inizio di ogni sessione di lavoro complessa.

---

## 1. Principi base

1. **Autocontenimento**: ogni prompt a un subagent include tutto il contesto necessario — il subagent non vede la conversazione corrente
2. **Single responsibility**: ogni subagent esegue un compito preciso e restituisce un risultato strutturato
3. **Verifica degli output**: Claude Code (primario) valida i risultati dei subagent prima di procedere
4. **Parallelismo sicuro**: i task implementativi paralleli usano worktree isolati per evitare conflitti di file
5. **Fallback esplicito**: se un subagent fallisce o restituisce null, Claude Code gestisce il caso prima di procedere

---

## 2. Taxonomy dei subagent

| Tipo | Agent tool type | Quando usarlo | Isolamento worktree |
|---|---|---|---|
| **research** | `Explore` | Esplorazione spec, ricerca simboli, mapping codebase | No |
| **plan** | `Plan` | Progettazione interfacce e API prima di scrivere codice | No |
| **implement** | default (`claude`) | Implementazione di uno o più deliverable | Sì (se parallelo) |
| **review** | `code-reviewer` | QA avversariale post-implementazione | No |

---

## 3. Flow di orchestrazione — task singolo

```
Claude Code (primario)
  ├── [opzionale] research subagent → comprende spec e pattern esistenti
  ├── [opzionale] plan subagent → progetta interfacce → propone a owner se architetturale
  ├── implement subagent → implementa deliverable → aggiorna IMPLEMENTATION_LOG
  └── [task critico] review subagent → verifica avversariale → PASS/FAIL/PARTIAL
```

Per task standard (già spec'd in TASK_QUEUE.md), si salta research e plan e si va diretto all'implementazione.

---

## 4. Flow di orchestrazione — task paralleli

```
Claude Code (primario)
  ├── Verifica indipendenza tra task (nessun file condiviso modificato)
  └── pipeline(tasks, task => implement_subagent(task, isolation='worktree'))
         ├── task A → worktree A → implementa M1-T3
         ├── task B → worktree B → implementa M1-T4
         └── [dopo completamento] review subagent su entrambi
```

**Quando è sicuro parallelizzare**: i task non modificano gli stessi file. Verificare prima controllando i deliverable richiesti.

**Quando NON parallelizzare**: task B dipende dall'output di task A (es. M1-T4 usa tipi definiti in M1-T3).

---

## 5. Template brief completi

### 5.1 Research (Explore type)

```
Read-only exploration del codebase TR4D3RZ in C:\projects\seq.
Profondità: [quick | medium | very thorough]

Obiettivo: [domanda specifica — es. "quali file definiscono il tipo GenomeCapsule?"]

Cerca in: [path — es. "tr4d3rz-core/src/"]

Contesto: [perché serve questa info — es. "devo implementare il subscriber MQTT che deserializza GenomeCapsule"]

Restituisci un report con: file trovati, definizioni rilevanti, pattern esistenti da riutilizzare.
```

### 5.2 Plan (Plan type)

```
Sei un Architecture Agent per TR4D3RZ.

Contesto del sistema:
- Milestone: M1 — Foundational Backbone Single RPi2
- Stack: Rust (core, messaging, persistence, evolution), TS/WASM (observatory)
- Contratti: C:\projects\seq\tr4d3rz-docs\protocols\MVP_INTERFACE_CONTRACTS.md
- ADR rilevanti: [lista]

Task da progettare: [descrizione]

Leggi prima:
- [spec file]
- [contratti rilevanti]

Produci:
1. Interfacce Rust (pub struct / pub trait) con docstrings
2. Schema dati (CBOR/JSON/SQLite) se applicabile
3. Topic MQTT se applicabile
4. Note su dipendenze con altri repository

NON scrivere implementazioni — solo interfacce e contratti.
Restituisci il design per approvazione.
```

### 5.3 Implement (default type, worktree se parallelo)

```
Stai lavorando su TR4D3RZ M1 milestone.
Repository: C:\projects\seq\[repo]
Task: [ID] — [titolo]

LEGGI PRIMA (obbligatorio, nell'ordine):
1. C:\projects\seq\tr4d3rz-docs\protocols\MVP_INTERFACE_CONTRACTS.md
2. C:\projects\seq\tr4d3rz-docs\COMMUNICATION\TASKS\[task-file].md
3. [spec aggiuntive se necessarie]

Implementa i seguenti deliverable:
| File | Descrizione |
|---|---|
| [percorso] | [cosa deve fare] |
| [percorso] | [cosa deve fare] |

Vincoli tecnici:
- [lista]

Definition of Done:
- [criterio verificabile — es. "cargo test passa", "tabella ha almeno 3 record"]

Al termine:
1. Aggiorna COMMUNICATION/IMPLEMENTATION_LOG.md aggiungendo una sezione con:
   - Scelte implementative non ovvie
   - Comandi per replicare il test
   - Limitazioni note
2. Aggiorna COMMUNICATION/TASKS/current_task.md → status: COMPLETED

Restituisci:
{
  "deliverables": ["file1", "file2"],
  "tests_run": ["cargo test -- --test-name", "..."],
  "test_results": "X/Y passing",
  "blockers": [],
  "notes": []
}
```

### 5.4 Review avversariale (code-reviewer type)

```
Sei un QA Agent avversariale per TR4D3RZ.

MINDSET: il tuo compito è trovare problemi, NON confermare che tutto vada bene.
Default: assume difetti fino a prova contraria. Sii distruttivo nelle assunzioni.

Componente: [nome componente]
Implementazione da rivedere:
- [file 1]
- [file 2]

Spec di riferimento:
- C:\projects\seq\tr4d3rz-docs\protocols\MVP_INTERFACE_CONTRACTS.md (sezione [X])
- [spec aggiuntive]

Checklist obbligatoria:
1. [ ] Conformità ai contratti MVP (topic MQTT, schema CBOR, campi SQLite)
2. [ ] Error handling — cosa succede se: broker MQTT non disponibile, DB pieno, payload malformato
3. [ ] Test coverage — quali scenari NON sono coperti dai test?
4. [ ] Vincoli hardware RPi2 — RAM, disk I/O, connessioni concorrenti
5. [ ] Idempotenza — rieseguire il binario è sicuro?

Restituisci:
{
  "verdict": "PASS" | "FAIL" | "PARTIAL",
  "findings": [
    { "severity": "HIGH|MEDIUM|LOW", "description": "...", "file": "...", "line": N, "fix": "..." }
  ],
  "uncovered_scenarios": [],
  "recommendation": "..."
}
```

---

## 6. Gestione risultati subagent

```
risultato = await implement_subagent(...)

if risultato == null:
    # Subagent fallito — non procedere
    log("Subagent fallito, riprovo con prompt semplificato o gestisco manualmente")
    return

if risultato.blockers.length > 0:
    # Blockers non risolti — riferire all'owner se architetturali
    proponi_a_owner(risultato.blockers)

if tipo_task == "critico":
    verdict = await review_subagent(risultato.deliverables)
    if verdict.verdict == "FAIL":
        fix_issues(verdict.findings)
        # Itera
```

---

## 7. Aggiornamento stato dopo ogni subagent

Dopo ogni implementazione completata, Claude Code aggiorna:

| File | Aggiornamento |
|---|---|
| `[repo]/COMMUNICATION/TASKS/current_task.md` | status: COMPLETED (fatto dal subagent o da Claude Code) |
| `[repo]/COMMUNICATION/IMPLEMENTATION_LOG.md` | Aggiunta sezione con scelte e test (fatto dal subagent) |
| `tr4d3rz-docs/COMMUNICATION/TASK_QUEUE.md` | Status task aggiornato (Claude Code primario) |
| `tr4d3rz-docs/DASHBOARD.md` | Snapshot stato progetto (Claude Code, ogni sessione) |

---

## 8. Session resumption — entry point

All'inizio di ogni sessione, Claude Code legge nell'ordine:

1. `tr4d3rz-docs/DASHBOARD.md` — stato globale in <5 min
2. `tr4d3rz-docs/COMMUNICATION/TASK_QUEUE.md` — task attivi e dipendenze
3. `[repo attivo]/COMMUNICATION/TASKS/current_task.md` — task corrente nel repo
4. `[repo attivo]/COMMUNICATION/IMPLEMENTATION_LOG.md` — contesto implementativo

Se DASHBOARD.md è stale (>2 giorni senza aggiornamento), aggiornarlo è la prima azione.

---

*Maintainer: Claude Code (Primary Agent) — Creato: 2026-07-15*
