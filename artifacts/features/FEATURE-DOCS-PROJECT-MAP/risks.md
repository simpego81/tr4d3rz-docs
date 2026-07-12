# Risk Register — FEATURE-DOCS-PROJECT-MAP

**Stato**: OPEN
**Owner del registro**: Manus
**Ultimo aggiornamento**: 2026-07-12
**Policy**: append-only; variazioni e chiusure devono essere aggiunte con data, motivazione ed evidenza.

## 1. Rischi attivi

| ID | Rischio | Probabilità | Impatto | Trigger osservabile | Mitigazione e gate | Owner | Residuo atteso |
|---|---|---:|---:|---|---|---|---:|
| R-PMAP-01 | Roadmap Markdown e nuova roadmap strutturata divergono | Alta | Critico | Differenza semantica tra YAML, Markdown e coda task | Unica SSOT YAML, Markdown generato, equivalence test; veto su consumer prima di schema e migrazione approvati | Manus | Basso |
| R-PMAP-02 | `.ecosystem` locale non è accessibile alla CI GitHub | Certa | Alto | Build remota priva del dataset agenti | Exporter locale allowlist-based, snapshot versionato, freshness badge e ultimo snapshot valido | Implementation Agent | Medio |
| R-PMAP-03 | Lo snapshot collaborativo pubblica testo sensibile o irrilevante | Media | Critico | Campo non previsto o testo libero compare nel JSON pubblico | Schema in allowlist, sanitizer, test privacy, revisione umana del primo snapshot; veto immediato su leakage | Manus / QA | Basso |
| R-PMAP-04 | Parser basati su Markdown o JavaScript embedded si rompono al variare del formato | Alta | Alto | `MAP-E004`, calo improvviso del conteggio entità | Preferire YAML/XML/JSON strutturati; parser con fixture reali, schema versionato e conteggi di regressione | Implementation Agent | Medio |
| R-PMAP-05 | Dati obsoleti appaiono autorevoli agli stakeholder | Alta | Alto | Timestamp oltre SLA senza segnalazione visibile | Freshness configurabile, badge `STALE`, manifest, ultimo aggiornamento e owner sempre visibili | Implementation Agent | Basso |
| R-PMAP-06 | Stati incoerenti tra roadmap, task queue e artefatti producono salute errata | Alta | Critico | Stesso ID con stati incompatibili o `COMPLETED` senza evidenza | Regole di conflitto esplicite; mai risolvere silenziosamente; degradare a `UNKNOWN` e bloccare i casi critici | Manus / QA | Medio |
| R-PMAP-07 | Grafi completi degradano performance e leggibilità | Media | Alto | Rendering lento, collisioni, interazioni non fluide o memoria elevata | Sintesi leggere in homepage, lazy loading, clustering, limite/virtualizzazione, performance budget e fallback tabellare | Visualization Agent | Medio |
| R-PMAP-08 | La homepage non è realmente utilizzabile da smartphone | Media | Alto | Overflow a 360 px, target touch piccoli, caricamento dei grafi completi | Mobile-first, card sintetiche, test 360/390 px, niente full graph iniziale, tap target e testo alternativo | Visualization Agent / QA | Basso |
| R-PMAP-09 | Le pagine di dettaglio desktop risultano rotte invece che intenzionalmente non responsive | Media | Medio | Controlli invisibili o contenuto troncato su viewport piccoli | Media query che mostra messaggio esplicito e accesso alla versione tabellare; nessuna promessa di editing mobile | Visualization Agent | Basso |
| R-PMAP-10 | Migrazione dell’attuale `index.html` rompe pagine o navigazione legacy | Media | Alto | Link 404, pagina device orfana, regressione del contenuto | Copia prima della sostituzione, link checker, inventory e smoke test; rollback immediato alla vecchia index | Implementation Agent / QA | Basso |
| R-PMAP-11 | Output generato parzialmente viene pubblicato | Media | Critico | File mancanti o manifest non coerente dopo errore/interruzione | Staging directory, validazione completa, rename atomico e ultimo snapshot valido; `MAP-E007` | Implementation Agent | Basso |
| R-PMAP-12 | Modifiche concorrenti nel repository sporco vengono incluse nel commit | Alta | Critico | `git diff --cached` contiene file non appartenenti alla feature | Branch/worktree isolato, allowlist di file, commit scoped, verifica pre-commit; veto se si toccano modifiche altrui | Manus | Basso |
| R-PMAP-13 | Dipendenza runtime da CDN rende le mappe fragili o introduce variazioni non controllate | Media | Medio | D3 non caricato, CSP/rete esterna indisponibile | Versione pin, asset vendorizzato o fallback locale, test senza rete esterna | Visualization Agent | Basso |
| R-PMAP-14 | Generazione di una pagina per nodo produce output eccessivo o route instabili | Media | Medio | Crescita anomala file, collisione slug, URL modificati al rename | ID stabili separati dalle label, route manifest, soglia dimensionale e generator test | Implementation Agent | Basso |
| R-PMAP-15 | Roadmap M2–M5 senza date suggerisce una precisione inesistente | Alta | Medio | Timeline posiziona automaticamente elementi non pianificati | `null` esplicito, corsia “non pianificata”, nessuna interpolazione o percentuale | Manus / Visualization Agent | Basso |
| R-PMAP-16 | Accessibilità del grafo dipende esclusivamente dal puntatore o dal colore | Media | Alto | Nodi non raggiungibili da tastiera o stati indistinguibili | Tabelle alternative, focus visibile, pattern/icone/testo, tooltip accessibili, audit keyboard e contrasto | Visualization Agent / QA | Basso |
| R-PMAP-17 | Il modello di salute diventa una seconda logica di gestione progetto | Media | Alto | UI modifica o interpreta stati senza fonte e senza regole versionate | Derivazioni pure e documentate, nessun editing UI, source_refs ed evidence obbligatori | Manus | Basso |
| R-PMAP-18 | GitHub Pages pubblica una build valida ma semanticamente incompleta | Media | Alto | Schema valido con zero nodi o calo drastico dei dataset | Soglie minime e regression counters nel manifest; approvazione manuale su variazioni anomale | QA / DevOps Agent | Medio |
| R-PMAP-19 | Nessun agente è attualmente autorizzato a scrivere codice in `tr4d3rz-docs` | Certa | Critico | Un task di implementazione viene assegnato a Claude Code o Antigravity senza modifica approvata di ruoli/repository | Risolvere in PMAP-00 con decisione esplicita dell’utente: autorizzazione scoped nel repository oppure pubblicazione cross-repo; aggiornare `AGENTS.md` prima del codice | Manus / User | Basso dopo approvazione |

## 2. Condizioni di veto

| Veto | Condizione | Azione richiesta |
|---|---|---|
| V-PMAP-01 | Implementazione avviata prima dell’approvazione di schema, ADR e migrazione roadmap | Fermare il task, creare conflitto e completare prima la SSOT |
| V-PMAP-02 | Dati collaborativi pubblicati senza sanitizer e allowlist | Bloccare build e rimuovere l’artefatto pubblico |
| V-PMAP-03 | `COMPLETED` o `HEALTHY` derivati senza evidenza verificabile | Degradare a `UNKNOWN`, correggere regola e aggiungere test |
| V-PMAP-04 | Homepage precedente rimossa o pagine legacy rese orfane | Rollback e ripetizione della migrazione con inventory/link report |
| V-PMAP-05 | Commit include modifiche concorrenti non appartenenti alla feature | Annullare staging, isolare worktree e ricreare commit scoped |
| V-PMAP-06 | Demo, QA indipendente o gate diagnostico non superati | Il task resta `IN_PROGRESS`; vietata la dichiarazione `COMPLETED` |
| V-PMAP-07 | Codice o output generato modificato in `tr4d3rz-docs` da un agente non autorizzato | Fermare l’implementazione, ripristinare l’ultimo baseline valido e ottenere una decisione owner con aggiornamento preventivo di `AGENTS.md` |

## 3. Assunzioni da monitorare

| ID | Assunzione | Confidenza | Evento che richiede revisione |
|---|---|---:|---|
| A-PMAP-01 | GitHub Pages continua a pubblicare contenuti statici da `main:/docs` | Alta | Modifica configurazione Pages o introduzione di build framework |
| A-PMAP-02 | D3 v7 è sufficiente per tutte e quattro le viste | Alta | Performance budget non rispettato o accessibilità non raggiungibile |
| A-PMAP-03 | La roadmap corrente è semanticamente importabile senza perdita | Media-alta | Conflitti non risolvibili tra roadmap, task queue e artefatti |
| A-PMAP-04 | Un exporter locale è accettabile per i dati `.ecosystem` | Alta | Richiesta di aggiornamento totalmente remoto o real-time |
| A-PMAP-05 | Le viste di dettaglio non richiedono piena responsività mobile | Confermata | Nuovo requisito esplicito degli stakeholder |

## 4. Registro variazioni

| Data | Evento | Impatto | Decisione |
|---|---|---|---|
| 2026-07-12 | Registro iniziale creato durante la pianificazione | Nessun codice implementato; rischio complessivo medio-alto per integrazione dati e migrazione | Procedere per milestone con SSOT e pipeline prima della UI |
| 2026-07-12 | Verificate le autorizzazioni in `AGENTS.md` | Manus non può scrivere codice; Claude Code e Antigravity non hanno `tr4d3rz-docs` tra i repository autorizzati | Aggiunto gate PMAP-00 e veto V-PMAP-07; richiesta decisione esplicita dell’utente prima dell’implementazione |

## Resolution events

### 2026-07-12 — R-PMAP-19 ownership gate resolved

L’owner del progetto ha approvato l’**opzione A**. `AGENTS.md` versione `1.0.0` autorizza Claude Code a implementare la pipeline dati/CI e Antigravity a implementare UI/D3 e demo direttamente in `tr4d3rz-docs`, esclusivamente per `FEATURE-DOCS-PROJECT-MAP`. GitHub Copilot mantiene la validazione indipendente e Manus resta privo di autorizzazione a scrivere codice. Il rischio passa da **ACTIVE/BLOCKING** a **CONTROLLED**; si riattiva se un agente modifica file fuori allowlist, lavora senza branch/worktree isolato o estende implicitamente l’autorizzazione ad altre feature.

### 2026-07-12 — Temporary workspace synchronization incident resolved

La disconnessione temporanea del computer assegnato è stata risolta dall’utente. Le copie locali di sicurezza sono state sincronizzate nel repository e gli artefatti sono nuovamente verificabili in `C:\projects\seq\tr4d3rz-docs`. L’incidente non modifica architettura o backlog; resta come evidenza del requisito di backup e sincronizzazione controllata.
