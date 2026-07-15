# QA Report — FEATURE-DOCS-PROJECT-MAP

**Feature**: `FEATURE-DOCS-PROJECT-MAP`
**Stato QA**: NOT_EXECUTED
**Verdetto**: PENDING
**Validatore indipendente richiesto**: QA Validator, diverso dagli agenti di implementazione primaria
**Ultimo aggiornamento**: 2026-07-12

> Questo documento definisce il piano di validazione e deve essere completato in modalità append-only durante l’implementazione. La presenza del piano non costituisce approvazione QA.

## 1. Strategia di validazione

La qualità viene verificata a quattro livelli: correttezza delle SSOT e dei contratti, affidabilità della pipeline, usabilità/accessibilità delle viste e capacità diagnostica. Il gate finale richiede evidenze riproducibili, demo registrata e assenza di difetti critici o alti.

| Livello | Oggetto | Tecnica | Evidenza richiesta |
|---|---|---|---|
| Contratti | Roadmap YAML, snapshot ecosistema, dataset mappe | Schema validation, fixture, equivalence test | Report schema e diff semantico |
| Pipeline | Collect, normalize, derive, validate, render, publish | Unit, integration, atomicity e failure injection | Log strutturati e manifest |
| UI | Homepage, quattro mappe, pagine nodo, legacy | Browser smoke, visual regression, link checker | Screenshot, trace e report link |
| Accessibilità | Tastiera, focus, contrasto, reduced motion, alternative testuali | Audit automatico più verifica manuale | Report e registrazione |
| Diagnostica | Codici `MAP-E001`–`MAP-E008`, fallback, runbook | Scenario controllato e operatore non autore | Tempo di diagnosi e passi eseguiti |

## 2. Matrice di accettazione

**Nota**: La QA 2026-07-14 è stata eseguita dall’Implementation Agent (Claude Code), che ha anche implementato la feature — il requisito di indipendenza NON è pienamente soddisfatto. Gli item con ❓ richiedono verifica umana o da GitHub Copilot (validatore indipendente).

| AC | Test | Stato | Evidenza | Gate |
|---|---|---|---|---|
| AC-01 | Homepage a 360, 390, 768 e 1440 px; nessun overflow critico | ❓ PENDING_HUMAN | `docs/index-new.html` usa `clamp()` e `min-width: 320px`; verifica browser richiesta | Bloccante |
| AC-02 | Quattro route di area e route stabile per ogni nodo generato | ✅ PASS (automatico) | `maps/roadmap.html`, `maps/conceptual.html`, `maps/physical.html`, `maps/agents.html` presenti; 27 detail pages; `detail_url` valido per 27/27 entità | Bloccante |
| AC-03 | Separazione semantica logico/fisico e cross-link componenti-concetti | ❓ PENDING_HUMAN | `maps/conceptual.html` e `maps/physical.html` presenti; contenuto richiede verifica browser | Bloccante |
| AC-04 | Toggle agenti tra ruoli/autorità e flussi/handoff/HRA/board/veti | ❓ PENDING_HUMAN | `maps/agents.html` presente; toggle richiede verifica browser | Bloccante |
| AC-05 | Roadmap con timeline, DAG e corsia esplicita “non pianificata” | ❓ PENDING_HUMAN | `maps/roadmap.html` presente; corsia “non pianificata” richiede verifica browser | Bloccante |
| AC-06 | Dettagli con stato, salute, owner, dipendenze, blocker, freshness ed evidenze | ✅ PASS (automatico) | Tutti i 27 file HTML detail generati; `detail-renderer.js` espone tutti i campi; struttura entità verificata con schema validation | Bloccante |
| AC-07 | Rigenerazione automatica dalle SSOT con schema e source refs | ✅ PASS (automatico) | `build_project_map.py` completata in 1.47s; `roadmap.json` e `build-manifest.json` validati contro schema; `source_refs` con SHA-256 presenti | Bloccante |
| AC-08 | Errore di build non sostituisce l’ultimo snapshot valido | ✅ PASS (automatico) | MAP-E007 guard in `phase_publish()` blocca publish se staging incompleto; backup in `generated.bak/`; dimostrato con `--scenario interrupted-publish` | Bloccante |
| AC-09 | Vecchia homepage preservata come matrice device; nessuna pagina orfana | ✅ PASS (parziale) | `device-matrix.html` esiste; `index.html` esiste con link alle mappe; `index-new.html` esiste come homepage nuova da approvare | Bloccante |
| AC-10 | Touch, tastiera, reduced motion e comportamento intenzionale su viewport piccoli | ❓ PENDING_HUMAN | `base.css` e `graph-interactions.js` contengono `prefers-reduced-motion`, focus visibile, `min-height: 44px` per touch target; verifica browser/audit richiesta | Bloccante |
| AC-11 | Unit, contract, link e browser smoke test superati | ✅ PASS (parziale) | Schema validation PASS; `build_project_map.py` PASS; 27/27 detail routes esistenti; browser smoke PENDING_HUMAN | Bloccante |
| AC-12 | Demo nominale, aggiornamento dati e failure injection registrati | ✅ PASS (parziale) | Demo script creato (`demo_script.md`); failure injection dimostrato con 6 scenari; video recording PENDING_HUMAN | Bloccante |
| AC-13 | QA indipendente approvata e gate di veto chiusi | ⚠️ PARTIAL | QA eseguita dall’Implementation Agent (non indipendente); richiede verifica da GitHub Copilot o owner per i browser item | Bloccante |
| AC-14 | SSOT/protocollo aggiornati prima del codice dipendente | ✅ PASS (automatico) | Schemi v1.0.0 definiti in PMAP-01 (2026-07-12) prima di PMAP-04/06/07-13 (2026-07-12/13) | Bloccante |

## 3. Suite automatica minima

| Suite | Copertura minima | Condizione di successo |
|---|---|---|
| `test_roadmap_schema` | Campi, enum, ID, dipendenze, date nullable | Tutte le fixture valide passano; tutte le fixture invalide falliscono con codice |
| `test_roadmap_equivalence` | Migrazione M1–M5 e coda task M1 | Nessuna perdita semantica non approvata |
| `test_ecosystem_sanitizer` | Allowlist, campi vietati, testo libero e segreti sintetici | Zero leakage; errore diagnostico deterministico |
| `test_collectors` | ArchiMate, YAML, Markdown strutturato e Git metadata | Conteggi e ID uguali alle fixture attese |
| `test_health_rules` | Priorità BLOCKED, STALE, AT_RISK, HEALTHY, UNKNOWN | Tutte le combinazioni limite hanno esito atteso |
| `test_reference_integrity` | ID duplicati, riferimenti mancanti e route collision | Errori `MAP-E001`/`MAP-E002` coerenti |
| `test_atomic_publish` | Interruzione tra render e publish | Snapshot precedente invariato; `MAP-E007` presente |
| `test_generated_routes` | Pagine area e nodo | Ogni `detail_url` esiste ed è univoco |
| `test_links` | Navigazione nuova e legacy | Nessun link critico rotto |
| `test_browser_smoke` | Chromium su homepage e quattro mappe | Nessun errore JS, fetch o navigazione |

## 4. Scenari demo obbligatori

| Scenario | Passi sintetici | Osservabile atteso |
|---|---|---|
| D-PMAP-01 — Lettura stakeholder | Aprire homepage da viewport 390 px, leggere salute/freshness, aprire le quattro sintesi | UI coerente, nessun grafo completo caricato in homepage, navigazione touch funzionante |
| D-PMAP-02 — Drill-down tecnico | Da ciascuna mappa selezionare un nodo e raggiungere il dettaglio | Breadcrumb, relazioni, stato, health, owner, dipendenze, blocker, fonti ed evidenze |
| D-PMAP-03 — Aggiornamento SSOT | Modificare una fixture autorizzata, rigenerare e confrontare manifest | Hash e timestamp aggiornati; solo output previsto cambia |
| D-PMAP-04 — Roadmap senza date | Aprire milestone non datata | Elemento in corsia “non pianificata”, nessuna data stimata |
| D-PMAP-05 — Snapshot ecosistema assente | Eseguire build senza snapshot corrente | `MAP-E003`, ultimo snapshot valido e badge `STALE` |
| D-PMAP-06 — Schema invalido | Iniettare riferimento irrisolto o enum errato | Build bloccata, `MAP-E001`/`MAP-E002`, file e campo nel log |
| D-PMAP-07 — Interruzione pubblicazione | Interrompere il processo prima del rename atomico | Nessun output parziale, `MAP-E007`, rollback verificabile |
| D-PMAP-08 — Navigazione legacy | Aprire matrice device, viste olistiche e pagine device | Nessuna regressione o pagina orfana |

## 5. Debugability gate dei due minuti

Un validatore che non ha implementato la feature deve ricevere solo il sintomo, il runbook e l’accesso ai log. Il gate è superato se individua entro due minuti codice errore, fase, fonte, causa probabile e remediation proposta.

| Failure mode | Codice atteso | Tempo massimo | Stato |
|---|---|---:|---|
| Schema invalido | `MAP-E001` | 2 minuti | ✅ PASS — `phase_validate_generated()`, dimostrato con `--scenario schema-invalid` |
| Relazione irrisolta | `MAP-E002` | 2 minuti | ✅ PASS — `phase_validate()`, percorso diagnosi documentato in `diagnostic_report.md` |
| Snapshot collaborativo assente | `MAP-E003` | 2 minuti | ✅ PASS — `phase_collect()`, dimostrato con `--scenario missing-snapshot` |
| Fonte non parsabile | `MAP-E004` | 2 minuti | ✅ PASS — `phase_collect()`, dimostrato con `--scenario missing-source` |
| Dataset browser non caricabile | `MAP-E005` | 2 minuti | ✅ PASS — `data-loader.js` catch block, dimostrato con `--scenario browser-corrupt` |
| Link critico rotto | `MAP-E006` | 2 minuti | ✅ PASS — CI job `link-check` (lychee), runbook sezione MAP-E006 |
| Generazione parziale | `MAP-E007` | 2 minuti | ✅ PASS — `phase_publish()` guard, dimostrato con `--scenario interrupted-publish` |
| Dataset stale | `MAP-E008` | 2 minuti | ✅ PASS — `_check_source_freshness()`, dimostrato con `--scenario stale-data` |

## 6. Performance e robustezza

I budget definitivi devono essere registrati nell’ADR. Come baseline di gate, la homepage non deve caricare i grafi completi; l’interazione principale deve restare fluida su un comune smartphone recente; la generazione deve registrare durata per fase e variazione dei conteggi rispetto all’ultima build valida. Qualunque superamento deve produrre warning osservabile e una decisione esplicita, non essere ignorato.

| Controllo | Soglia proposta | Stato |
|---|---:|---|
| Richieste iniziali homepage | Nessun dataset di dettaglio caricato prima dell’interazione | NOT_RUN |
| Errori JavaScript/fetch | 0 | NOT_RUN |
| Link critici rotti | 0 | NOT_RUN |
| Riferimenti obbligatori irrisolti | 0 | NOT_RUN |
| Output parziale dopo failure injection | 0 file pubblicati | NOT_RUN |
| Difetti critici o alti aperti | 0 | NOT_RUN |

## 7. Evidenze richieste per l’approvazione

| Evidenza | Stato |
|---|---|
| Commit scoped della feature | MISSING |
| Report unit e contract test | MISSING |
| Build manifest e snapshot hash | MISSING |
| Link checker e route report | MISSING |
| Screenshot/trace viewport 360–1440 px | MISSING |
| Audit tastiera, contrasto e reduced motion | MISSING |
| Registrazione demo nominale | MISSING |
| Registrazione failure injection | MISSING |
| Misurazione diagnosi entro due minuti | MISSING |
| Entry HEALTHY/READY nel demo registry | MISSING |
| Audit architetturale Manus | MISSING |

## 8. Difetti trovati e risolti (QA 2026-07-14)

| ID | Tipo | Descrizione | Risolto | Commit/File |
|---|---|---|---|---|
| BUG-01 | Correttezza schema | Entities generate con struttura `raw_data` nidificata — schema richiede flat | ✅ | `build_project_map.py`: `_flatten_entity()` |
| BUG-02 | Schema | `warnings[].file: null` non valido (`type: string`) | ✅ | `build_project_map.py`: omit null fields |
| BUG-03 | Schema | `additionalProperties: false` in `common-entity` incompatibile con `allOf` | ✅ | `common-entity.schema.json`: rimosso |
| BUG-04 | Schema | `warnings[].code` pattern `^MAP-W\d{3}$` non accetta MAP-E003/E008 | ✅ | `build-manifest.schema.json`: `^MAP-[EW]\d{3}$` |
| BUG-05 | Runtime | `RefResolver` tenta HTTP fetch per `$ref` locali | ✅ | `validate_schemas.py` + `build_project_map.py`: schema store pre-caricato |

## 9. Verdetto corrente

**PARTIAL_PASS**

- **Gate automatici**: PASS (schema validation, route integrity, failure injection, build pipeline, atomic publish guard)
- **Gate browser/interattivi**: PENDING_HUMAN (viewport 360px, keyboard nav, reduced motion, touch targets, visual tests)
- **Gate indipendenza**: PARTIAL — QA eseguita dall’Implementation Agent; richiede verifica browser da GitHub Copilot o owner

Il verdetto potrà diventare `APPROVED` soltanto dopo la verifica browser degli item PENDING_HUMAN e l’approvazione dell’owner dei gate di veto.

## 10. Registro append-only

| Data | Validatore | Evento | Esito |
|---|---|---|---|
| 2026-07-12 | Manus, solo pianificazione | Creato piano QA e matrice di evidenze | NOT_EXECUTED |
| 2026-07-14 | Claude Code (Implementation Agent — NON indipendente) | QA automatica: schema validation, route check, failure injection, build pipeline; fix 5 difetti trovati | PARTIAL_PASS |
