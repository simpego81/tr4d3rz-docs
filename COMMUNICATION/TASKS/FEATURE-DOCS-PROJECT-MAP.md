# TASK — FEATURE-DOCS-PROJECT-MAP

**Titolo**: Homepage GitHub Pages “Project Map”
**Assegnato da**: Manus, Chief Architect & Coordinator
**Repository target**: `tr4d3rz-docs`
**Stato**: COMPLETED (FUNCTIONALLY COMPLETE — browser gate PENDING_HUMAN)
**Data assegnazione**: 2026-07-12
**Spec autoritativa**: `artifacts/features/FEATURE-DOCS-PROJECT-MAP/spec.md`
**Backlog autoritativo**: `artifacts/features/FEATURE-DOCS-PROJECT-MAP/tasks.yaml`
**Autorizzazione scoped**: `AGENTS.md`, versione `1.0.0`

---

## 1. Obiettivo

Sostituire l’attuale homepage GitHub Pages con una mappa progressiva dell’intero progetto. Il primo livello, mobile-first, deve offrire quattro viste sintetiche interattive: ecosistema concettuale, ecosistema fisico, setup collaborativo degli agenti e roadmap. Ogni vista deve condurre a una pagina dedicata e ogni nodo deve poter condurre a un dettaglio stabile con stato, salute, owner, dipendenze, blocker, ultimo aggiornamento, evidenze e riferimenti alle SSOT.

L’attuale homepage non deve essere rimossa. Deve essere trasferita a `docs/device-matrix.html`, contestualizzata come matrice dell’ecosistema fisico e preservata nella navigazione e nei test di regressione.

> La UI è una proiezione delle SSOT. Non può diventare una fonte concorrente né introdurre date, percentuali o stati non supportati da evidenze.

## 2. Ownership approvata

L’owner ha approvato l’**opzione A** il 2026-07-12. L’implementazione avviene direttamente in `tr4d3rz-docs` con permessi limitati alla feature.

| Agente | Responsabilità scoped | Task principali |
|---|---|---|
| Claude Code | Roadmap strutturata, snapshot sanificato, pipeline dati, schemi, generatori, test, CI, diagnostica, migrazione legacy **e** design system, shell UI, homepage, pagine progressive, quattro mappe D3, accessibilità, test interattivi e demo | `PMAP-02..16`, `PMAP-18` |
| GitHub Copilot | Validazione indipendente, verifica dei tool, report QA e controllo diagnostico | `PMAP-17` |
| Manus | Architettura, coordinamento, ADR, autorizzazioni, veti, audit degli artefatti e chiusura | `PMAP-00`, `PMAP-01`, `PMAP-19` |

> **Nota**: Antigravity ha lasciato il team il 2026-07-13. I task `PMAP-07..13` e `PMAP-18` sono stati trasferiti a Claude Code. Autorizzazione aggiornata in `AGENTS.md` v1.1.0.

Ogni agente deve usare un branch o worktree isolato e rispettare l’allowlist dei file del task. Nessuna autorizzazione si estende ad altre feature. Manus non scrive codice.

## 3. Sequenza obbligatoria

| Ordine | Milestone | Contenuto | Gate di uscita |
|---|---|---|---|
| 1 | `PMAP-M0` | ADR, modello canonico, roadmap YAML e snapshot collaborativo | Contratti approvati prima dei consumer |
| 2 | `PMAP-M1` | Collector, normalizer, health engine, validazione e publish atomico | Dataset deterministici, schema-validi e diagnosticabili |
| 3 | `PMAP-M2` | Design system, shell progressiva, pagine dettaglio e homepage preview | Fixture complete, fallback statico e accessibilità base |
| 4 | `PMAP-M3` | Mappe concettuale, fisica, agenti e roadmap | Test semantici, drill-down e cross-link superati |
| 5 | `PMAP-M4` | Migrazione device matrix, CI, deploy preview e rollback | Nessuna regressione e rollback provato |
| 6 | `PMAP-M5` | QA indipendente, demo registrata, audit e chiusura | Tutti i gate soddisfatti |

L’implementazione frontend non può precedere schema, fixture canoniche e contratti delle route. Le dipendenze esatte e gli output sono definiti in `tasks.yaml`.

## 4. Deliverable obbligatori

| Area | Deliverable |
|---|---|
| Homepage | `docs/index.html` con quattro sintesi interattive, stato globale e freshness |
| Pagine area | `docs/maps/conceptual.html`, `physical.html`, `agents.html`, `roadmap.html` |
| Dettagli | `docs/details/<kind>/<stable-id>.html` generati con route stabili |
| Legacy | `docs/device-matrix.html` con la homepage corrente ricontestualizzata |
| Dati | Dataset canonici in `docs/data/generated/` e manifest di build |
| SSOT roadmap | `state/roadmap.yaml`, con `state/roadmap.md` come vista generata |
| Pipeline | Collector, normalizer, validator, health engine, renderer, test e CI |
| Operazioni | Runbook, codici `MAP-E001`–`MAP-E008`, log strutturati e metriche |
| Evidenze | QA report, demo registrata, implementation log e commit scoped |

## 5. Vincoli funzionali e UX

La homepage deve essere mobile-first per stakeholder tecnici e non tecnici. Le pagine di dettaglio possono essere desktop-oriented, ma su schermi piccoli devono preservare breadcrumb, sintesi e fallback tabellare. Le visualizzazioni interattive devono offrire ricerca, filtri, zoom/pan, focus, deep-link e navigazione da tastiera. I grafi completi devono essere caricati soltanto nelle pagine dedicate; la homepage usa preview leggere.

Le quattro viste devono rispettare la separazione semantica. La mappa concettuale non mostra componenti fisici. La mappa fisica mostra componenti e rimandi espliciti ai concetti implementati. La mappa agenti presenta sia ruoli e autorità sia flussi di handoff, HRA, board e veti. La roadmap mostra timeline e DAG delle dipendenze senza inventare date mancanti.

## 6. Stato, salute e provenienza

Ogni dettaglio deve esporre `status`, `health`, `owner`, `dependencies`, `blockers`, `updated_at`, `evidence`, `source_refs` e `detail_url`. La salute usa esclusivamente `HEALTHY`, `AT_RISK`, `BLOCKED`, `STALE` e `UNKNOWN`. Le regole di derivazione devono essere versionate, testate e accompagnate dalla provenienza delle fonti.

`COMPLETED` non può essere inferito senza evidenza. Conflitti fra SSOT producono diagnostica e non vengono risolti silenziosamente. In caso di errore critico, la build deve conservare l’ultimo snapshot valido.

## 7. QA, demo e debugability

| Gate | Condizione minima |
|---|---|
| Unit e schema | Tutti i test della pipeline passano e gli errori indicano file, campo e codice |
| Integrazione | Output deterministico, riferimenti risolti, route e link validi |
| UI | Tutte le mappe supportano drill-down, deep-link e fallback tabellare |
| Accessibilità | Tastiera, focus visibile, contrasto, reduced motion e target touch verificati |
| Regressione | Pagine legacy raggiungibili e device matrix preservata |
| Sicurezza | Snapshot `.ecosystem` allowlist-based e privo di dati non pubblicabili |
| Debugability | Un operatore non autore identifica fase, fonte, causa e remediation entro due minuti |
| Demo | Scenario funzionante, osservabile e registrato in `state/demo_registry.md` |

La demo deve comprendere almeno happy path, drill-down nelle quattro viste, stato di salute con evidenze, snapshot stale, conflitto di fonte, schema invalido, link rotto e rollback sull’ultimo snapshot valido.

## 8. Protocollo di avanzamento

Il task master e ciascun task in `tasks.yaml` seguono esclusivamente `PENDING → IN_PROGRESS → COMPLETED`. Gli agenti devono aggiornare `current_task.md`, `COMMUNICATION/IMPLEMENTATION_LOG.md` e gli artefatti di feature. Un handoff incompleto, una modifica fuori allowlist o un protocollo modificato senza aggiornamento preventivo della SSOT determinano veto.

La feature non può essere dichiarata `COMPLETED` senza commit scoped, stato e log aggiornati, `spec.md`, `tasks.yaml`, `risks.md` e `qa_report.md` completi, QA indipendente approvata, demo validata e gate di debugability superato.

## 9. Riferimenti

1. `artifacts/features/FEATURE-DOCS-PROJECT-MAP/implementation_plan.md`
2. `artifacts/features/FEATURE-DOCS-PROJECT-MAP/migration_plan.md`
3. `artifacts/features/FEATURE-DOCS-PROJECT-MAP/risks.md`
4. `artifacts/features/FEATURE-DOCS-PROJECT-MAP/qa_report.md`
5. `AGENTS.md`

---

*Approvazione architetturale: Manus — 2026-07-12*
*Decisione di ownership: owner del progetto — opzione A, 2026-07-12*
