# TR4D3RZ Project Dashboard

**Purpose**: Rapid project re-entry after inattività (target: <5 min)  
**Maintainer**: Claude Code (Primary Agent)  
**Last Updated**: 2026-07-15  
**Auto-Update**: Dopo ogni task completato o cambio di stato significativo

---

## Stato Globale

| Dimensione | Status | Note |
|---|---|---|
| **Architettura** | HEALTHY | Fondamenta solide; topologia Single RPi2 consolidata |
| **M1 Progress** | IN PROGRESS — 57% | 4/7 task completati; T3 parziale |
| **Agenti** | SEMPLIFICATO | Modello single primary (Claude Code) + subagent interni |
| **Documentazione** | AGGIORNATA | AGENTS.md, SUBAGENT_PROTOCOL.md, DASHBOARD aggiornati oggi |
| **Blockers** | NESSUNO | Tutti i gate precedenti risolti |

---

## Focus Corrente

### Milestone Attiva: **M1 — Foundational Backbone Single RPi2**

**Completamento**: 57% (4/7 task — se T3 parziale conta come 0.5 → ~4.5/7)

### Stato Task M1

| Task | Repo | Status | Note |
|---|---|---|---|
| M1-T0 | tr4d3rz-docs | COMPLETED | Spec, protocolli, contratti MVP |
| M1-T1 | tr4d3rz-core | COMPLETED | Tipi Rust condivisi (8/8 test) |
| M1-T2 | tr4d3rz-messaging | COMPLETED | MQTT library Rust (12/13 test) |
| M1-T2-B | tr4d3rz-messaging | COMPLETED | Heartbeat Probe validato su RPi2 |
| **M1-T3** | tr4d3rz-persistence | **IN_PROGRESS (PARTIAL)** | Library esistente (event_logger, schema, lib); **manca**: main.rs (subscriber MQTT), config/, systemd/, migrations/ |
| M1-T4 | tr4d3rz-evolution | PENDING | Repo vuoto, dipendenze soddisfatte |
| M1-T5 | tr4d3rz-embedded | PENDING | Simulatore/firmware ESP8266; gate M1-T2-B soddisfatto |
| M1-T6 | tr4d3rz-observatory | BLOCKED | Dipende da M1-T2 + M1-T3 |
| M1-T7 | cross-repo | BLOCKED | Dipende da tutti i precedenti |

### FEATURE-DOCS-PROJECT-MAP

| Status | Gate |
|---|---|
| FUNCTIONALLY COMPLETE (19/20 task) | Browser validation gate PENDING_HUMAN — richiede verifica manuale viewport e keyboard nav su `docs/index-new.html` e `maps/*.html` |

---

## Roadmap

| Milestone | Status | Target |
|---|---|---|
| M0 — Foundations | COMPLETED | — |
| **M1 — MVP Backbone** | IN PROGRESS (57%) | Corrente |
| M2 — Basic Evolution | PENDING | Q3 2026 |
| M3 — Cooperative Ecology | PENDING | Q4 2026 |
| M4 — Full Observatory | PENDING | Q1 2027 |
| M5 — Production | PENDING | Q2 2027 |

**Critical path M1**: T3 (completa) → T4 → T5 → T6 → T7

---

## Modello Agenti (aggiornato 2026-07-15)

**Prima**: Manus (Chief Architect esterno) + Claude Code + GitHub Copilot + Antigravity + HRA  
**Ora**: Claude Code (tutti i ruoli) + Subagent interni + User come approver

| Chi | Ruolo |
|---|---|
| **User (Owner)** | Approva proposte architetturali e priorità |
| **Claude Code** | Orchestrazione, implementazione, QA, doc, meta-optimizer, librarian, embedded |
| **Subagent interni** | Spawned da Claude Code: research / plan / implement / review |

Documentazione: `AGENTS.md`, `SUBAGENT_PROTOCOL.md`

---

## Repository Status

| Repository | Stato | Ultimo Task |
|---|---|---|
| `tr4d3rz-docs` | ACTIVE | Ristrutturazione collaborazione (2026-07-15) |
| `tr4d3rz-core` | READY | M1-T1 completato (commit e8ecad4) |
| `tr4d3rz-messaging` | READY | M1-T2 + T2-B completati (commit af19bee) |
| `tr4d3rz-persistence` | IN_PROGRESS (PARTIAL) | Library esistente, binary mancante |
| `tr4d3rz-evolution` | PENDING | Non iniziato |
| `tr4d3rz-observatory` | BLOCKED | Dipende da T3 |
| `tr4d3rz-embedded` | PENDING | Pronto per simulatore ESP8266 |

---

## Rischi Attivi

| Rischio | Probabilità | Impatto | Mitigation |
|---|---|---|---|
| T3 parziale blocca T6 | MEDIO | ALTO | Completare main.rs subscriber come prossimo task |
| ESP8266 memory constraints | MEDIO | MEDIO | Minimize payload, no_std Rust |
| Observatory performance | BASSO | MEDIO | Deferred a M1-T6 |

---

## Navigazione Rapida per Task Comuni

### Riprendo dopo una pausa — cosa faccio?
1. Leggi questo file (stato globale)
2. Leggi `COMMUNICATION/TASK_QUEUE.md` (dipendenze e prossimi task)
3. Leggi `[repo attivo]/COMMUNICATION/TASKS/current_task.md`
4. Leggi `[repo attivo]/COMMUNICATION/IMPLEMENTATION_LOG.md`

### Sto implementando un task — cosa mi serve?
1. Spec → `specs/[component]/` o `COMMUNICATION/TASKS/[task].md`
2. Contratti → `protocols/MVP_INTERFACE_CONTRACTS.md`
3. ADR rilevanti → `adr/`
4. Protocollo subagent → `SUBAGENT_PROTOCOL.md`

### Voglio fare QA su un'implementazione
1. Leggi `SUBAGENT_PROTOCOL.md` §5.4 (template review avversariale)
2. Spawna un review subagent (code-reviewer type)
3. Valida il risultato — PASS / FAIL / PARTIAL

---

## Quick Reference

| Risorsa | Path |
|---|---|
| Ruoli e subagent | `AGENTS.md`, `SUBAGENT_PROTOCOL.md` |
| Task attivi | `COMMUNICATION/TASK_QUEUE.md` |
| Contratti MVP | `protocols/MVP_INTERFACE_CONTRACTS.md` |
| Topic MQTT | `protocols/mqtt-topic-structure.md` |
| ADR | `adr/` |
| Spec per componente | `specs/[component]/` |
| Knowledge Base index | `KNOWLEDGE_BASE.md` |
| Convergence metrics | `state/meta_metrics.md` |

---

## Azioni Immediate — Prossima Sessione

### FEATURE-VIEWS (priorità corrente)
1. **`scripts/build_views.py`** — script Python che legge `state/roadmap.yaml` + `state/agent_activity.json` e genera `docs/data/stakeholder_data.json`, `docs/data/roadmap_data.json`, `docs/views/roadmap.html`, `docs/views/architecture.html`
2. **Update `stakeholders.html`** — fetch `../data/stakeholder_data.json` al load → badge overlay "M1: 57%" in sezione 1
3. **Update CI/CD** — esegue `build_views.py` su ogni push

### Poi M1
4. **Completare M1-T3**: `main.rs` subscriber MQTT → SQLite, `config/persistence.toml`, `systemd/` unit
5. **Browser validation gate FEATURE-DOCS-PROJECT-MAP**: richiede verifica manuale su browser

## FEATURE-VIEWS — Stato al 2026-07-15

| Pagina | Stato |
|---|---|
| `docs/views/stakeholders.html` | IN_PROGRESS — animazione Three.js implementata, review visiva in corso |
| `docs/views/process.html` | DONE — D3 Gantt, legge agent_activity.json |
| `docs/views/roadmap.html` | PENDING |
| `docs/views/architecture.html` | PENDING |
| Pipeline CI/CD views | PENDING |

---

*Dashboard Maintainer: Claude Code (Primary Agent)*  
*Target Re-Entry Time: <5 minuti*
