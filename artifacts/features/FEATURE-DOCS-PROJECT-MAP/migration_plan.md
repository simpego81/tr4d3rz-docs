# Migration Plan — FEATURE-DOCS-PROJECT-MAP

**Stato**: PENDING
**Owner architetturale**: Manus
**Data**: 2026-07-12

## 1. Principio di migrazione

La migrazione è incrementale e reversibile. Nessun consumer deve dipendere dal nuovo formato prima che la SSOT, lo schema, il changelog e la documentazione di migrazione siano stati approvati. Durante la transizione, le viste umane preesistenti restano disponibili e l’ultimo dataset valido continua a essere pubblicato.

## 2. Sequenza vincolante

| Ordine | Cambiamento | Output | Gate |
|---:|---|---|---|
| 1 | Approvare ADR e contratto dati delle mappe | ADR, JSON Schema, vocabolari di stato/salute | Veto Gate 0: nessun codice consumer prima dell’approvazione |
| 2 | Ufficializzare `state/roadmap.yaml` | Schema roadmap, versione, changelog, guida di migrazione | Equivalenza semantica con `state/roadmap.md` corrente |
| 3 | Generare `state/roadmap.md` dal YAML | Vista umana riproducibile | Diff revisionato; nessuna perdita di milestone o stato |
| 4 | Definire l’export sanificato di `.ecosystem` | Contratto snapshot, allowlist dei campi, manifest | Revisione privacy e assenza di contenuti sensibili |
| 5 | Costruire collector, normalizer e validator | Dataset in staging e report diagnostico | Unit e contract test al 100% |
| 6 | Generare dettagli e viste interattive senza cambiare entry point | Preview locale isolata | Demo nominale e failure injection validate |
| 7 | Spostare l’attuale homepage a `device-matrix.html` | Pagina legacy contestualizzata | Link checker e confronto contenuti |
| 8 | Attivare la nuova `index.html` | Homepage centrale | Smoke test 360 px, desktop e navigazione tastiera |
| 9 | Abilitare deploy e monitoraggio freshness | Workflow e runbook | QA indipendente, demo registry, debug gate |

## 3. Strategia roadmap

`state/roadmap.yaml` diventa la rappresentazione canonica. La versione iniziale deve importare integralmente M1–M5 senza inventare date. I task dettagliati M1 possono essere derivati dalla coda corrente; gli elementi successivi privi di date conservano `start: null` ed `end: null`.

| Campo canonico | Origine iniziale | Regola di conflitto |
|---|---|---|
| Milestone e outcome | `state/roadmap.md` | La roadmap prevale sulla coda task per il perimetro di milestone |
| Task M1 e dipendenze | `COMMUNICATION/TASK_QUEUE.md` | Una divergenza genera errore di validazione, non una scelta silenziosa |
| Owner | Coda task e matrici ruoli | Owner mancante produce warning e `UNKNOWN` |
| Stato | Artefatti feature e coda task | Un `COMPLETED` senza evidenza è degradato a `UNKNOWN` con errore diagnostico |
| Evidenze | QA report, demo registry, commit e log | Solo link verificabili e relativi al workspace/repository |
| Date | Valori espliciti nella SSOT | Nessuna data viene stimata dal generatore |

## 4. Strategia homepage

L’attuale homepage deve essere copiata, non riscritta in-place come primo passo. La nuova pagina viene sviluppata e dimostrata in una route di preview; solo dopo la validazione la preview diventa `docs/index.html`.

| Artefatto corrente | Destinazione | Compatibilità richiesta |
|---|---|---|
| `docs/index.html` | `docs/device-matrix.html` | Stesso contenuto funzionale, titolo e contesto aggiornati |
| `docs/holistic_view.html` | Conservata e collegata | Nessuna regressione; può diventare vista legacy/avanzata |
| `docs/<device>.html` | Invariata | Raggiungibile dalla matrice e dalle pagine di dettaglio |
| `docs/archimate_data.json` | Conservato durante la transizione | Il nuovo generatore può importarlo, ma non deve dipendere da JavaScript embedded |
| Nuova homepage preview | `docs/_preview/project-map/index.html` durante lo sviluppo | Non sostituisce l’entry point fino al gate QA |

## 5. Rollback

Il rollback deve poter essere eseguito ripristinando la precedente `index.html` e l’ultimo snapshot valido, senza rigenerare i dati. La pipeline conserva manifest e hash dell’ultima pubblicazione valida. Se il deploy introduce errori critici, la procedura documentata deve completarsi in meno di dieci minuti e lasciare un codice evento `MAP-E007` nei log.

## 6. Condizioni di completamento della migrazione

La migrazione è completata soltanto quando nuova homepage, quattro pagine di area, pagine nodo, dataset e generatori sono versionati; la roadmap YAML è ufficiale e la vista Markdown è generata; la vecchia homepage è preservata; link checker e browser smoke test passano; demo e failure injection sono registrate; QA indipendente e gate di debugability sono approvati.
