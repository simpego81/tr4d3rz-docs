# Piano architetturale — Homepage GitHub Pages “Project Map”

**Feature**: `FEATURE-DOCS-PROJECT-MAP`
**Autore**: Manus AI
**Stato**: PENDING
**Data**: 2026-07-12

## Executive summary

La homepage di `tr4d3rz-docs` verrà sostituita da una mappa progressiva dell’intero progetto, destinata sia a stakeholder non tecnici sia a stakeholder tecnici. Il primo livello sarà mobile-first e presenterà quattro sintesi interattive: ecosistema logico, ecosistema fisico, setup collaborativo degli agenti e roadmap. Ogni sintesi condurrà a una pagina di area dedicata; ogni nodo condurrà a una pagina di dettaglio stabile con stato, salute, owner, dipendenze, blocker, ultimo aggiornamento, evidenze e fonti.

L’attuale homepage non verrà eliminata: sarà trasferita a `docs/device-matrix.html`, contestualizzata come matrice dell’ecosistema fisico e mantenuta nella navigazione insieme alle pagine device e alla vista olistica esistenti.

> La UI sarà una proiezione delle SSOT, non una nuova fonte di verità. Tutti i dati saranno estratti, normalizzati, validati e sintetizzati da tool software deterministici.

## Architettura informativa

| Livello | Route | Contenuto | Target |
|---|---|---|---|
| Homepage | `docs/index.html` | Quattro sintesi, stato globale, freshness e accesso ai dettagli | Tecnico e non tecnico; mobile-first |
| Mappa concettuale | `docs/maps/conceptual.html` | Domini, concetti logici e relazioni, senza componenti fisici | Desktop-oriented |
| Mappa fisica | `docs/maps/physical.html` | Device, nodi, repository, runtime e collegamenti ai concetti implementati | Desktop-oriented |
| Mappa agenti | `docs/maps/agents.html` | Livello 1: ruoli e autorità; livello 2: handoff, HRA, board, veti e repository | Desktop-oriented |
| Roadmap | `docs/maps/roadmap.html` | Timeline e grafo delle dipendenze sincronizzati | Desktop-oriented |
| Dettaglio nodo | `docs/details/<kind>/<stable-id>.html` | Stato, health, owner, dipendenze, blocker, evidenze e fonti | Desktop-oriented |
| Legacy | `docs/device-matrix.html` | Homepage attuale ricontestualizzata | Compatibilità |

Le pagine di dettaglio non richiedono piena responsività mobile. Su viewport piccoli devono tuttavia restare leggibili almeno breadcrumb, sintesi e versione tabellare, con un messaggio esplicito che raccomanda uno schermo più ampio per il grafo completo.

## Modello dati e salute

La UI consumerà dataset JSON generati in `docs/data/generated/`. Ogni entità avrà ID stabile, tipo, nome, sintesi, stato, salute, owner, dipendenze, blocker, timestamp, evidenze, riferimenti alle fonti e URL di dettaglio.

| Dimensione | Valori |
|---|---|
| Stato | `PLANNED`, `READY`, `IN_PROGRESS`, `BLOCKED`, `COMPLETED`, `DEPRECATED`, `UNKNOWN` |
| Salute | `HEALTHY`, `AT_RISK`, `BLOCKED`, `STALE`, `UNKNOWN` |

La salute sarà derivata con priorità esplicita: un blocco critico produce `BLOCKED`; una fonte oltre soglia produce `STALE`; dipendenze non soddisfatte o rischio alto producono `AT_RISK`; dati coerenti, aggiornati e provati producono `HEALTHY`; dati insufficienti o conflittuali producono `UNKNOWN`. `COMPLETED` non sarà mai inferito senza evidenza.

## Fonti autoritative

| Vista | SSOT primaria | Integrazioni |
|---|---|---|
| Concettuale | Modello ArchiMate e contratti in `tr4d3rz-docs` | ADR, specifiche, knowledge base |
| Fisica | Modello ArchiMate e `specs/node-software-map.md` | Inventory, pagine device, metadati repository |
| Agenti | `.ecosystem/README.md`, mandato, emendamento e regole | Snapshot sanificato di board, ruoli e flussi |
| Roadmap | Nuovo `state/roadmap.yaml` | Task queue, feature artifact, demo registry |
| Health/evidenze | Project state, risk register, QA report, demo registry e Git | Build manifest e validazioni |

La roadmap corrente in Markdown verrà migrata a YAML machine-readable. Il Markdown diventerà una vista generata, così da evitare due roadmap concorrenti. Le milestone prive di date resteranno esplicitamente “non pianificate”; il sistema non inventerà date né percentuali di avanzamento.

## Pipeline automatica

| Fase | Responsabilità | Gate |
|---|---|---|
| Collect | Leggere roadmap, ArchiMate, Markdown strutturato, metadati Git e snapshot agenti | Fonti dichiarate e hash registrati |
| Normalize | Produrre entità e relazioni canoniche con ID stabili | Nessuna precedenza silenziosa sui conflitti |
| Validate | Applicare schema, enum, integrità dei riferimenti, route e link | Errori critici bloccano la build |
| Derive | Calcolare health, freshness, percorso critico e sintesi | Regole versionate e testate |
| Render | Generare JSON e pagine statiche in staging | Output completo prima del publish |
| Publish | Sostituzione atomica dell’ultimo snapshot valido | Nessun dataset parziale pubblicato |

La build resterà compatibile con GitHub Pages statico. Un wrapper PowerShell manterrà la continuità con il flusso corrente; parsing e validazione saranno implementati preferibilmente in Python 3 per portabilità e testabilità. Poiché `.ecosystem` è locale, un exporter allowlist-based produrrà uno snapshot sanificato versionato; la CI lo convaliderà senza richiedere accesso al filesystem locale.

## UX e tecnologia

D3 v7 verrà usato attraverso moduli condivisi, non tramite implementazioni duplicate. La homepage caricherà solo preview leggere; i grafi completi saranno caricati entrando nelle pagine di area. Tutte le viste offriranno ricerca, filtri, zoom/pan, focus, collegamenti profondi e fallback tabellare. Tastiera, focus visibile, reduced motion, contrasto e target touch sono gate obbligatori.

| Vista | Rappresentazione |
|---|---|
| Concettuale | Grafo a cluster o livelli logici |
| Fisica | Topologia stratificata con cross-link ai concetti |
| Agenti | Due modalità sincronizzate: role map e flow map |
| Roadmap | Timeline più DAG delle dipendenze |

## Migrazione e rollback

La nuova homepage verrà sviluppata inizialmente sotto una route di preview. Soltanto dopo demo e QA verrà promossa a `docs/index.html`. La homepage corrente sarà copiata prima della sostituzione, i link relativi saranno verificati e un inventory test impedirà pagine orfane.

Il rollback ripristinerà la precedente index e l’ultimo snapshot valido senza rigenerazione. La pipeline registrerà manifest, hash, fase e codici diagnostici `MAP-E001`–`MAP-E008`.

## Ownership approvata

L’owner del progetto ha approvato il **12 luglio 2026** l’opzione A: implementazione scoped direttamente in `tr4d3rz-docs`. Claude Code è autorizzato, esclusivamente per questa feature, a realizzare roadmap strutturata, snapshot sanificato, pipeline dati, schemi, generatori, test, CI, diagnostica e migrazione legacy. Antigravity è autorizzato a realizzare design system, UI/D3, homepage, mappe, pagine progressive, test di interazione/accessibilità e demo. GitHub Copilot esegue la validazione indipendente. Manus non scrive codice e conserva architettura, coordinamento, veti e gate di chiusura.

L’autorizzazione è versionata in `AGENTS.md` come `1.0.0`, termina con PMAP-19 o per revoca dell’owner e non estende i permessi ad altri file o feature. Ogni agente opera su branch o worktree isolato e con allowlist dei file assegnati.

## Piano per milestone

| Milestone | Contenuto | Exit gate |
|---|---|---|
| M0 — Protocolli e SSOT | ADR, schema, roadmap YAML, snapshot collaborativo | Contratti approvati prima dei consumer |
| M1 — Data pipeline | Collector, normalizer, health engine, validazione e publish atomico | Dataset deterministici e failure injection |
| M2 — UI progressiva | Design system, homepage e pagine nodo generate | Funzionamento con fixture e accessibilità base |
| M3 — Mappe | Concettuale, fisica, agenti e roadmap | Acceptance test semantici e interattivi |
| M4 — Migrazione | Device matrix, link legacy, CI e deploy preview | Nessuna regressione e rollback provato |
| M5 — QA e demo | Runbook, test indipendenti, demo registrata, audit Manus | Tutti i gate, commit e stato aggiornati |

Il backlog eseguibile comprende venti task ordinati, da `PMAP-00` a `PMAP-19`, con dipendenze, owner, output e criteri di accettazione. L’implementazione non può iniziare dal frontend: i primi task obbligatori sono SSOT, schema, migrazione roadmap e snapshot sanificato.

## Debuggability e failure mode

| Codice | Failure mode | Comportamento |
|---|---|---|
| `MAP-E001` | Schema invalido | Build bloccata con file e campo |
| `MAP-E002` | ID duplicato o relazione irrisolta | Build bloccata con entità coinvolte |
| `MAP-E003` | Snapshot agenti assente | Ultimo snapshot valido e badge `STALE` |
| `MAP-E004` | Fonte non parsabile | Errore o warning secondo criticità |
| `MAP-E005` | Dataset non caricabile nel browser | Fallback statico e diagnostica visibile |
| `MAP-E006` | Link critico rotto | Report link e blocco deploy |
| `MAP-E007` | Generazione parziale | Output valido invariato e rollback |
| `MAP-E008` | Dataset oltre freshness SLA | UI disponibile con warning e owner |

La feature supera il gate diagnostico solo se un operatore non autore identifica codice, fase, fonte, causa e remediation entro due minuti.

## Decisioni e rischi principali

Non restano decisioni bloccanti: l’owner ha approvato l’autorizzazione scoped dell’opzione A. Branding e date future possono evolvere come configurazione e dati. I rischi più rilevanti sono divergenza delle SSOT, leakage dallo snapshot collaborativo, parsing fragile, dati stale presentati come affidabili, regressione dei link legacy, pubblicazione parziale e contaminazione del commit da modifiche concorrenti. Tutti hanno trigger, mitigazioni e condizioni di veto nel risk register.

## Criterio di completamento

La feature potrà passare a `COMPLETED` esclusivamente con commit scoped, stato e implementation log aggiornati, quattro artefatti completi e append-only, QA indipendente approvata, demo scenario-based registrata, vecchia homepage preservata, protocollo/SSOT aggiornati prima del codice e gate di debugability superato.

## Artefatti del piano

| Artefatto | Contenuto |
|---|---|
| `spec.md` | Architettura, modello dati, UX, pipeline e criteri di accettazione |
| `tasks.yaml` | Backlog eseguibile con milestone e dipendenze |
| `risks.md` | Rischi, trigger, mitigazioni, assunzioni e veti |
| `qa_report.md` | Piano QA, matrice test, demo e debug gate |
| `migration_plan.md` | Sequenza SSOT-first, migrazione homepage e rollback |
| `implementation_plan.md` | Sintesi decisionale, milestone, ownership e strategia operativa |

## Riferimenti interni

1. `tr4d3rz-docs/state/roadmap.md` — roadmap corrente.
2. `tr4d3rz-docs/COMMUNICATION/TASK_QUEUE.md` — stato e dipendenze operative.
3. `tr4d3rz-docs/state/project_state.md` — stato sintetico.
4. `tr4d3rz-docs/state/demo_registry.md` — evidenze demo.
5. `tr4d3rz-docs/specs/node-software-map.md` — relazione nodi/software.
6. `tr4d3rz-docs/docs/index.html` — homepage corrente da preservare.
7. `tr4d3rz-docs/docs/holistic_view.html` — vista interattiva esistente.
8. `.ecosystem/README.md` — modello collaborativo autoritativo.
9. `AMENDMENT_TO_METAMODEL.md` e `METAMODEL_TRANSITION_MANDATE.md` — autorità e vincoli del setup agenti.
