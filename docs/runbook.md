# Project Map — Runbook operativo

**Sistema**: TR4D3RZ Project Map (FEATURE-DOCS-PROJECT-MAP)  
**Versione runbook**: 1.0.0  
**Mantenuto da**: Debug Intelligence Agent (Claude Code)  
**Obiettivo**: Consentire a un operatore non autore di identificare causa e remediation in meno di 2 minuti.

---

## Come usare questo runbook

1. Individua il codice errore nel log di build (`MAP-E001`–`MAP-E008`)
2. Vai alla sezione corrispondente
3. Segui i passi di diagnosi e remediation

Se il build non ha prodotto alcun output o si è interrotto senza codice, vai a **MAP-E007**.

---

## Dove trovare i log

| Contesto | Posizione log |
|---|---|
| CI GitHub Actions | Tab **Actions** → workflow run → job `build` → step "Build project map data" |
| Build locale | Output di `python scripts/build_project_map.py --verbose` |
| Manifest generato | `docs/data/generated/build-manifest.json` → campi `errors` e `warnings` |
| Backup pre-publish | `docs/data/generated.bak/build-manifest.json` |

---

## MAP-E001 — Schema validation failed

**Sintomo**: Il build termina con exit code 1. Il log contiene `[MAP-E001]`.

**Causa**: Un dataset generato (es. `roadmap.json`) non rispetta il proprio JSON Schema.

**Diagnosi (< 2 min)**:
```
[MAP-E001] Generated 'roadmap.json' fails schema validation at milestones -> 0 -> status: 'INVALID_ENUM_VALUE' is not one of [...]
  Phase: validate
  File: .../staging/roadmap.json
```
1. Leggi il campo `message` nel log — indica il path nel JSON e il valore non valido
2. Apri `state/roadmap.yaml` e cerca il valore segnalato
3. Confronta con i valori consentiti in `artifacts/features/FEATURE-DOCS-PROJECT-MAP/schemas/roadmap.schema.json`

**Remediation**:
- Correggi il valore in `state/roadmap.yaml` (o nella fonte segnalata)
- Riesegui `python scripts/build_project_map.py --verbose`
- Se lo schema è sbagliato (non il dato), aggiorna lo schema e aggiorna `schemas/CHANGELOG.md`

---

## MAP-E002 — Duplicate entity ID

**Sintomo**: Il build termina con exit code 1. Il log contiene `[MAP-E002]`.

**Causa**: Due entità nella pipeline normalizzata condividono lo stesso ID (kebab-case).

**Diagnosi (< 2 min)**:
```
[MAP-E002] Duplicate entity ID: m1-t3-event-persistence
  Phase: validate
```
1. Cerca l'ID duplicato in `state/roadmap.yaml` (sezione `tasks`)
2. Cerca anche in `docs/archimate_data.json` se il duplicato viene da ArchiMate

**Remediation**:
- Rinomina uno dei due: cambia `id` o `slug` nella fonte YAML/JSON
- Riesegui il build

---

## MAP-E003 — Ecosystem snapshot absent

**Sintomo**: Il build termina con exit code 2 (warnings). Il log contiene `[MAP-E003]`. Il manifest mostra `freshness_status: "STALE"`.

**Causa**: Il file `artifacts/features/FEATURE-DOCS-PROJECT-MAP/ecosystem-snapshot.json` non è presente.

**Diagnosi (< 2 min)**:
```
[!] [MAP-E003] Ecosystem snapshot absent — collaborative system data unavailable.
    File: .../ecosystem-snapshot.json
```
1. Verifica che `ecosystem-snapshot.json` esista nella directory sopra indicata
2. Se assente: l'agente locale deve rigenerarlo

**Remediation**:
```bash
# Dalla root di tr4d3rz-docs, con .ecosystem/ presente in locale:
python scripts/export_ecosystem_snapshot.py
git add artifacts/features/FEATURE-DOCS-PROJECT-MAP/ecosystem-snapshot.json
git commit -m "chore: refresh ecosystem snapshot"
git push
```
> In CI il file viene letto dalla versione committata. Se il file è assente nel repo, il badge STALE comparirà su tutte le viste agente fino al prossimo commit.

---

## MAP-E004 — Source not parseable / missing

**Sintomo**: Il build termina con exit code 1. Il log contiene `[MAP-E004]`.

**Causa**: Una fonte obbligatoria (`state/roadmap.yaml`) non è trovata o non è parsabile.

**Diagnosi (< 2 min)**:
```
[CRITICAL ERROR] [MAP-E004] Required source 'roadmap' not found or unparsable
  Phase: collect
  File: .../state/roadmap.yaml
```
1. Verifica che `state/roadmap.yaml` esista
2. Testa il parse manualmente: `python -c "import yaml; yaml.safe_load(open('state/roadmap.yaml'))"`

**Remediation**:
- Se il file è assente: ripristinalo da git (`git checkout HEAD -- state/roadmap.yaml`)
- Se è malformato: correggi l'indentazione YAML (errore più comune: tab invece di spazi)
- Riesegui il build

---

## MAP-E005 — Browser dataset not loadable

**Sintomo**: La mappa o la homepage si apre ma mostra solo il fallback statico. La console del browser mostra un errore di parsing JSON.

**Causa**: `docs/data/generated/roadmap.json` è corrotto o assente (errore lato browser, non lato pipeline).

**Diagnosi (< 2 min)**:
1. Apri la DevTools del browser → Console → cerca `SyntaxError` o `fetch error`
2. Verifica il file: `python -c "import json; json.load(open('docs/data/generated/roadmap.json'))"`

**Remediation**:
```bash
python scripts/build_project_map.py --verbose
git add docs/data/generated/
git commit -m "fix: regenerate corrupted dataset"
git push
```

---

## MAP-E006 — Critical link broken

**Sintomo**: Il job `link-check` del workflow CI fallisce. Il log mostra uno o più URL con status 4xx.

**Causa**: Un link `href` in un file HTML di `docs/` punta a una risorsa inesistente (pagina rimossa, slug cambiato).

**Diagnosi (< 2 min)**:
```
[ERROR] docs/maps/roadmap.html#anchor → 404: target fragment not found
```
1. Leggi l'output di lychee nel CI — indica file sorgente e target mancante
2. Cerca il link nel file segnalato: `grep -n "href.*target-slug" docs/maps/roadmap.html`

**Remediation**:
- Se la pagina di destinazione è stata rinominata: aggiorna il link
- Se la pagina è stata rimossa: rimuovi il link o punta a un'alternativa
- Per i link a `detail/` pages: riesegui `python scripts/generate_detail_pages.py` se il file di dettaglio manca

---

## MAP-E007 — Partial generation / interrupted publish

**Sintomo**: Il build termina con exit code 1. Il log contiene `[MAP-E007]`. Nessun file è stato scritto in `docs/data/generated/` (il backup `.bak` è integro).

**Causa**: La staging directory era incompleta prima del rename atomico (file mancante, processo interrotto).

**Diagnosi (< 2 min)**:
```
[CRITICAL ERROR] [MAP-E007] Incomplete staging — missing: build-manifest.json. Publish aborted.
  Phase: publish
```
1. Verifica la staging directory: `ls artifacts/features/FEATURE-DOCS-PROJECT-MAP/staging/`
2. Verifica il backup: `ls docs/data/generated.bak/`

**Remediation**:
- Il backup in `docs/data/generated.bak/` è integro — il publish precedente è sicuro
- Correggi la causa (es. disco pieno, permessi) e riesegui il build completo
- Non spostare manualmente file da `.bak/` a `generated/` — il build atomico lo farà correttamente

---

## MAP-E008 — Source data stale

**Sintomo**: Il build termina con exit code 2 (warnings). Il log contiene `[MAP-E008]`. Il manifest mostra `freshness_status: "STALE"`.

**Causa**: Un file sorgente non è stato aggiornato entro il threshold configurato in `config/freshness_policy.yaml`.

**Diagnosi (< 2 min)**:
```
[!] [MAP-E008] Source 'ecosystem_snapshot' is stale: last modified 48h ago (threshold: 24h).
    File: .../ecosystem-snapshot.json
```
1. Leggi il messaggio: indica quale fonte è stale e da quanto
2. Controlla la policy: `cat config/freshness_policy.yaml`

**Remediation**:
- Per `ecosystem_snapshot`: riesporta e committa (vedi MAP-E003)
- Per `roadmap`: aggiorna `state/roadmap.yaml` e committa
- Se la soglia è troppo stringente, modifica `config/freshness_policy.yaml` e aggiorna `schemas/CHANGELOG.md`

---

## Checklist rapida (< 5 min da zero)

```
1. Apri il log CI o esegui: python scripts/build_project_map.py --verbose
2. Cerca "MAP-E" nel output
3. Vai alla sezione corrispondente in questo runbook
4. Segui Diagnosi → Remediation
5. Riesegui il build per confermare la risoluzione
```

---

## Test di failure injection

Per dimostrare ogni scenario in modo controllato:

```bash
# Lista scenari disponibili
python scripts/ci/failure_injection.py --list

# Esegui un singolo scenario (backup+iniezione+build+ripristino automatico)
python scripts/ci/failure_injection.py --scenario missing-snapshot
python scripts/ci/failure_injection.py --scenario schema-invalid
python scripts/ci/failure_injection.py --scenario stale-data
python scripts/ci/failure_injection.py --scenario missing-source
python scripts/ci/failure_injection.py --scenario browser-corrupt
python scripts/ci/failure_injection.py --scenario interrupted-publish
```

> Lo script esegue il backup automatico e ripristina sempre il file originale, anche in caso di errore.

---

## Contatti e escalation

| Ruolo | Responsabilità | Come contattare |
|---|---|---|
| Debug Intelligence Agent | Diagnosi e runbook | Claude Code (questo runbook) |
| Implementation Agent | Fix pipeline e schema | Claude Code |
| Chief Architect | Decisioni architetturali | Manus (tr4d3rz-docs owner) |
| QA Validator | Validazione indipendente | GitHub Copilot |

---

*Runbook generato per PMAP-16 — Debug Intelligence Agent*  
*Ultima revisione: 2026-07-14*
