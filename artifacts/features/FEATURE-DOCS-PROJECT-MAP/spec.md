# Feature Specification — FEATURE-DOCS-PROJECT-MAP

**Titolo**: Homepage GitHub Pages con mappa progressiva dell’ecosistema TR4D3RZ
**Architect**: Manus
**Owner implementativi approvati**: Claude Code per pipeline dati/CI, UI/D3 e demo (Antigravity uscita dal team 2026-07-13); GitHub Copilot per validazione indipendente
**Stato**: PENDING
**Ultimo aggiornamento**: 2026-07-12
**Repository**: `tr4d3rz-docs`

---

## 1. Obiettivo

La feature sostituisce l’attuale homepage GitHub Pages con un punto di ingresso centrale, comprensibile sia agli stakeholder non tecnici sia agli stakeholder tecnici. La pagina deve offrire una lettura progressiva dell’ecosistema attraverso quattro mappe sintetiche interattive: ecosistema logico, ecosistema fisico, setup collaborativo degli agenti e roadmap.

L’attuale homepage non viene eliminata. Deve essere spostata e ricontestualizzata come pagina della matrice dei dispositivi fisici, mantenendo raggiungibili tutte le pagine per-device e la vista olistica già esistente.

> Principio architetturale: la UI non è una nuova fonte di verità. Ogni dato visualizzato deve essere derivato da una SSOT identificabile, accompagnato da origine, data di aggiornamento ed evidenze.

## 2. Risultato atteso

| Livello | Pubblico | Contenuto | Requisito responsive |
|---|---|---|---|
| Homepage | Tecnico e non tecnico | Quattro sintesi, stato globale, freshness, accesso ai dettagli | Mobile-first da 360 px, tablet e desktop |
| Pagina di area | Prevalentemente tecnico | Grafo completo, filtri, legenda, stato e salute | Desktop-oriented; su mobile è ammesso un invito a usare uno schermo più grande |
| Pagina di nodo | Tecnico | Dati, relazioni, owner, dipendenze, blocker, evidenze e fonti | Desktop-oriented |
| Evidenza sorgente | Tecnico/audit | Documento, artefatto, demo, commit o report di origine | Dipende dall’artefatto |

## 3. Architettura informativa

La nuova `docs/index.html` presenta quattro moduli visuali. Ogni modulo contiene una sintesi interattiva leggera, una breve descrizione in linguaggio non tecnico, indicatori di stato/freshness e un collegamento alla rispettiva pagina di area.

| Area | Route proposta | Sintesi in homepage | Pagina di area | Drill-down per nodo |
|---|---|---|---|---|
| Ecosistema concettuale | `maps/conceptual.html` | Domini e concetti logici, senza nodi o repository fisici | Grafo logico completo con relazioni semantiche | `details/concepts/<stable-id>.html` |
| Ecosistema fisico | `maps/physical.html` | Nodi, repository, runtime e device principali | Topologia fisica con rimandi ai concetti implementati | `details/components/<stable-id>.html` |
| Collaborazione agenti | `maps/agents.html` | Ruoli, autorità e responsabilità principali | Due livelli: ruoli/poteri e flussi di handoff, HRA, board, veti e repository | `details/roles/<stable-id>.html` |
| Roadmap | `maps/roadmap.html` | Milestone, stato, percorso critico e prossimi outcome | Timeline più grafo delle dipendenze | `details/roadmap/<stable-id>.html` |

La navigazione deve consentire il ritorno stabile al livello precedente, mantenere filtri e selezione quando possibile tramite query string o fragment, e rendere ogni nodo direttamente linkabile.

## 4. Modello dati pubblico

La UI consuma esclusivamente dataset JSON validati e pubblicati in `docs/data/generated/`. Il contratto minimo comune a ogni entità è il seguente.

| Campo | Tipo | Obbligatorio | Significato |
|---|---|---:|---|
| `id` | stringa stabile | sì | Identificatore non dipendente dall’etichetta visuale |
| `kind` | enum | sì | `concept`, `component`, `role`, `milestone`, `task` o sottotipo versionato |
| `name` | stringa | sì | Etichetta umana |
| `summary` | stringa | sì | Sintesi non tecnica, breve e priva di markup non sicuro |
| `status` | enum | sì | `PLANNED`, `READY`, `IN_PROGRESS`, `BLOCKED`, `COMPLETED`, `DEPRECATED`, `UNKNOWN` |
| `health` | enum | sì | `HEALTHY`, `AT_RISK`, `BLOCKED`, `STALE`, `UNKNOWN` |
| `owners` | array | sì | Ruoli o agenti responsabili; può essere vuoto solo con warning |
| `dependencies` | array di ID | sì | Dipendenze dichiarate e risolte dal validatore |
| `blockers` | array | sì | Blocchi attivi con severità e riferimento |
| `updated_at` | timestamp ISO 8601 | sì | Ultima modifica della fonte autoritativa |
| `evidence` | array | sì | Link a demo, report, commit, artefatti o documenti verificabili |
| `source_refs` | array | sì | Percorsi SSOT che hanno prodotto l’entità |
| `detail_url` | URL relativa | sì | Pagina di dettaglio generata |

I dataset iniziali sono `conceptual-map.json`, `physical-map.json`, `agent-map.json`, `roadmap.json`, `health-summary.json` e `build-manifest.json`. Quest’ultimo registra versione schema, data di generazione, commit del repository, hash delle fonti, warning, errori non fatali e data dell’ultimo snapshot valido.

## 5. Regole di stato, salute e freshness

**Stato** descrive il ciclo di vita dichiarato dalla SSOT; **salute** descrive l’affidabilità operativa del dato e delle sue dipendenze. Le due dimensioni non devono essere fuse.

| Priorità | Condizione | Salute derivata |
|---:|---|---|
| 1 | Stato `BLOCKED` oppure blocker critico attivo | `BLOCKED` |
| 2 | Fonte oltre la soglia di freshness prevista e stato non terminale | `STALE` |
| 3 | Dipendenza obbligatoria `BLOCKED`, `UNKNOWN` o non risolta; rischio alto non mitigato | `AT_RISK` |
| 4 | Stato coerente, fonti valide, dipendenze soddisfatte ed evidenze presenti | `HEALTHY` |
| 5 | Dati insufficienti o conflittuali | `UNKNOWN` |

Le soglie di freshness devono essere configurabili per tipo di fonte in un file versionato, non codificate nella UI. La homepage deve mostrare sempre la data dell’ultimo aggiornamento valido e un badge di staleness. In caso di errore di generazione non deve essere pubblicato un dataset parziale: resta servito l’ultimo snapshot valido, accompagnato da warning visibile.

## 6. Fonti autoritative e responsabilità

| Vista | Fonte primaria | Fonti integrative | Note di normalizzazione |
|---|---|---|---|
| Concettuale | Modello ArchiMate e contratti in `tr4d3rz-docs` | ADR, specifiche e knowledge base | Escludere repository, host e device dalla vista logica |
| Fisica | Modello ArchiMate, `specs/node-software-map.md`, metadati repository | Pagine per-device e inventory | Ogni componente fisico deve referenziare i concetti logici implementati |
| Agenti | `.ecosystem/README.md`, mandato, emendamento e regole | Board cognitivi, matrice ruoli/repository, conflitti | `.ecosystem` è locale: pubblicare solo snapshot sanificati e privi di contenuto sensibile |
| Roadmap | `state/roadmap.yaml` proposto come SSOT machine-readable | `TASK_QUEUE.md`, milestone, feature artifact e demo registry | `state/roadmap.md` diventa vista umana generata, non fonte concorrente |
| Salute/evidenze | Stato progetto, rischi, demo registry, QA report e Git metadata | Build manifest e validazioni schema | Non dedurre `COMPLETED` senza evidenza e gate coerenti |

## 7. Pipeline di estrazione e pubblicazione

La soluzione deve mantenere GitHub Pages statico. L’automazione proposta è un processo deterministico articolato in sei passaggi.

| Passaggio | Responsabilità | Output o gate |
|---|---|---|
| 1. Collect | Leggere le SSOT dichiarate e gli snapshot esterni autorizzati | Modelli sorgente in memoria, nessuna modifica ai file |
| 2. Normalize | Convertire Markdown, YAML, ArchiMate/XML e metadati Git nel modello canonico | Entità e relazioni con ID stabili |
| 3. Validate | Verificare schema, ID duplicati, riferimenti, enum, URL locali e campi obbligatori | Build bloccata sugli errori; warning espliciti sui dati incompleti |
| 4. Derive | Calcolare salute, freshness, percorsi critici e sintesi | Dataset derivati riproducibili |
| 5. Render | Generare JSON pubblico e pagine di dettaglio statiche | Output in directory temporanea |
| 6. Publish | Sostituzione atomica di `docs/data/generated/` e dei dettagli generati | Mai lasciare output parziali; mantenere ultimo snapshot valido |

L’exporter locale deve poter accedere a `C:\projects\seq\.ecosystem` e produrre uno snapshot sanificato nel repository. La CI GitHub valida lo snapshot e gli altri dati già versionati, rigenera le pagine e impedisce il deploy in caso di schema non valido. La pipeline deve supportare almeno Windows/PowerShell, perché il generatore corrente è PowerShell; la logica di parsing e validazione dovrebbe tuttavia essere implementata in un runtime portabile e testabile, preferibilmente Python 3, invocato dal wrapper PowerShell.

### 7.1 Policy di fallback

Un fallimento dell’export locale o della build non deve rendere la homepage inutilizzabile. La UI carica `build-manifest.json`; se il dataset corrente è mancante o invalido, mostra l’ultimo snapshot valido. Se anche quello non è disponibile, presenta contenuto statico minimo, collegamenti alle SSOT e il codice diagnostico dell’errore.

## 8. Interazioni e visual design

La homepage usa progressive disclosure: titoli e spiegazioni comprensibili, badge compatti, micro-legende e interazioni touch. I grafi completi vengono caricati solo entrando nelle pagine di area, riducendo peso e complessità su smartphone.

| Vista | Modello interattivo raccomandato | Interazioni minime |
|---|---|---|
| Concettuale | Grafo a cluster o livelli logici | Zoom, pan, focus, ricerca, filtri per dominio, apertura nodo |
| Fisica | Grafo topologico stratificato | Filtri per tipo/device/repository, evidenziazione del concetto implementato, apertura nodo |
| Agenti | Diagramma a due modalità: role map e flow map | Toggle livello, filtri per ruolo/repository, evidenziazione di handoff e veto |
| Roadmap | Timeline sincronizzata con DAG delle dipendenze | Filtro milestone/stato/owner, percorso critico, apertura task o milestone |

D3 v7 può essere riutilizzato, ma il codice deve essere modulare e non duplicato tra pagine. Tutte le viste devono offrire un’alternativa testuale/tabellare, navigazione da tastiera, focus visibile, tooltip accessibili, supporto a `prefers-reduced-motion` e target touch adeguati.

## 9. Migrazione della homepage corrente

| Passo | Azione | Vincolo di compatibilità |
|---:|---|---|
| 1 | Copiare l’attuale `docs/index.html` in `docs/device-matrix.html` | Nessuna perdita di contenuto o link alle pagine device |
| 2 | Aggiornare i link relativi e il titolo per contestualizzarla come matrice fisica | I collegamenti per-device devono restare validi |
| 3 | Creare la nuova `docs/index.html` | Mantenere `index.html` come entry point Pages |
| 4 | Collegare la matrice, `holistic_view.html` e le pagine legacy dalle nuove mappe | Nessuna pagina preesistente diventa orfana |
| 5 | Aggiungere test automatici dei link e smoke test visuali | Deploy bloccato per link critici rotti |

## 10. Roadmap come SSOT strutturata

La roadmap ufficiale esiste già in `state/roadmap.md`, ma il formato corrente non contiene in modo uniforme dipendenze, finestre temporali, owner, evidenze e relazioni tra milestone. La feature deve introdurre `state/roadmap.yaml` come SSOT versionata e machine-readable, accompagnata da schema, changelog e migrazione. `state/roadmap.md` deve essere rigenerata dal file YAML per preservare la lettura umana e impedire divergenze.

Ogni milestone e task deve avere almeno ID stabile, titolo, outcome, stato, owner, dipendenze, eventuali date o intervalli, blocker, evidenze, ultimo aggiornamento e fonte. Le date mancanti devono restare `null` e venire visualizzate come “non pianificata”, senza stime inventate.

## 11. Debuggability by Design

| Codice | Failure mode | Comportamento atteso | Diagnosi entro due minuti |
|---|---|---|---|
| `MAP-E001` | Schema JSON/YAML non valido | Build fallita prima della pubblicazione | File, campo e posizione nel log |
| `MAP-E002` | ID duplicato o relazione irrisolta | Build fallita | Entità e riferimenti coinvolti |
| `MAP-E003` | Snapshot `.ecosystem` assente | Ultimo snapshot valido più badge `STALE` | Manifest indica path e timestamp attesi |
| `MAP-E004` | Fonte Markdown non parsabile | Build fallita o warning secondo criticità | Parser, file e sezione coinvolta |
| `MAP-E005` | Dataset non caricabile nel browser | Fallback statico | Console e pannello diagnostico con URL e status |
| `MAP-E006` | Link/evidenza locale rotta | Warning o build failure per link critico | Report dei link con sorgente e target |
| `MAP-E007` | Generazione parziale | Nessuna sostituzione dell’output valido | Log della staging directory e rollback |
| `MAP-E008` | Dataset oltre freshness SLA | UI disponibile con badge `STALE` | Timestamp fonte, soglia e owner |

Il generatore deve produrre log strutturati, riepilogo conteggi, durata per fase, numero di warning/errori, hash input/output e runbook. La demo deve consentire di iniettare almeno un errore controllato e osservare fallback, codice e log.

## 12. Criteri di accettazione

| ID | Criterio verificabile |
|---|---|
| AC-01 | `docs/index.html` mostra le quattro sintesi e funziona a 360 px senza overflow orizzontale critico |
| AC-02 | Ogni sintesi conduce a una pagina di area dedicata e ogni nodo conduce a una pagina di dettaglio stabile |
| AC-03 | La mappa concettuale non mostra componenti fisici; la mappa fisica collega ogni componente ai concetti implementati |
| AC-04 | La mappa agenti offre una vista ruoli/autorità e una vista flussi/handoff/HRA/board/veti |
| AC-05 | La roadmap mostra timeline e dipendenze, senza inventare date mancanti |
| AC-06 | Stato, salute, owner, dipendenze, blocker, ultimo aggiornamento ed evidenze sono disponibili nei dettagli; nessuna percentuale è mostrata |
| AC-07 | I dati pubblicati sono prodotti automaticamente dalle SSOT e validati contro schema |
| AC-08 | Un errore di generazione non pubblica output parziale e non rende la homepage inutilizzabile |
| AC-09 | L’attuale homepage è preservata come `device-matrix.html` e tutte le pagine preesistenti restano raggiungibili |
| AC-10 | La homepage è utilizzabile con touch, tastiera e reduced motion; le pagine desktop mostrano un messaggio intenzionale su viewport piccoli |
| AC-11 | La suite include unit test dei parser/derivazioni, contract test JSON, link checker e smoke test browser |
| AC-12 | La demo registrata esegue scenario nominale, drill-down, aggiornamento dati e failure injection con diagnosi entro due minuti |
| AC-13 | `qa_report.md` è approvato da validatore indipendente e tutti i gate di veto risultano superati |
| AC-14 | Roadmap e protocollo di pubblicazione sono aggiornati nella SSOT con versione, changelog, dipendenze e note di migrazione prima del codice dipendente |

## 13. Non obiettivi

La feature non sostituisce l’Observatory runtime e non introduce telemetria live. Non richiede editing visuale delle SSOT dalla UI, autenticazione, backend dinamico o database. Non promette responsività completa delle viste di dettaglio su smartphone. Non calcola percentuali di avanzamento e non usa inferenze non tracciabili per colmare dati mancanti.

## 14. Dipendenze e decisioni residue

| Elemento | Stato | Decisione |
|---|---|---|
| GitHub Pages da `main:/docs` | Confermato | Conservare il modello statico |
| D3 v7 e vista olistica corrente | Disponibili | Riutilizzare pattern e dati validi, non il parsing fragile di JavaScript embedded |
| Roadmap ufficiale | Esistente ma poco strutturata | Migrare a YAML canonico più Markdown generato |
| Snapshot `.ecosystem` | Non pubblicabile direttamente da CI | Export locale sanificato più validazione CI |
| Branding definitivo | Non specificato | Usare design system sobrio derivato dall’identità attuale; palette e token centralizzati e facilmente sostituibili |
| Date M2–M5 | Non affidabili o assenti | Visualizzare come non pianificate finché l’utente o la SSOT non le definiscono |

Non restano decisioni bloccanti per avviare l’implementazione. Branding e date future possono evolvere attraverso dati/configurazione senza modificare l’architettura.

## 15. Riferimenti interni

1. [`state/roadmap.md`](../../../state/roadmap.md) — roadmap umana corrente.
2. [`COMMUNICATION/TASK_QUEUE.md`](../../../COMMUNICATION/TASK_QUEUE.md) — dipendenze e stato M1.
3. [`state/project_state.md`](../../../state/project_state.md) — stato sintetico del progetto.
4. [`state/demo_registry.md`](../../../state/demo_registry.md) — evidenze demo e osservabilità.
5. [`specs/node-software-map.md`](../../../specs/node-software-map.md) — relazione nodi/software.
6. [`specs/observatory/holistic-view-generation-spec.md`](../../../specs/observatory/holistic-view-generation-spec.md) — precedente D3 data-driven.
7. [`scripts/generate_holistic_data.ps1`](../../../scripts/generate_holistic_data.ps1) — generatore corrente dei dati olistici.
8. [`docs/index.html`](../../../docs/index.html) — homepage da preservare e ricontestualizzare.
9. [`docs/holistic_view.html`](../../../docs/holistic_view.html) — vista interattiva esistente.
10. [`.ecosystem/README.md`](../../../../.ecosystem/README.md) — modello collaborativo autoritativo locale.
