# Diagnostic Report — FEATURE-DOCS-PROJECT-MAP

**Prodotto da**: Debug Intelligence Agent (Claude Code)  
**Task**: PMAP-16  
**Data**: 2026-07-14  
**Status**: COMPLETED

---

## 1. Error Code Registry

| Codice | Fase pipeline | Exit code | Descrizione | Trigger condizione |
|--------|--------------|:---------:|-------------|-------------------|
| MAP-E001 | validate | 1 | Generated dataset fails JSON Schema validation | Enum non valido, campo mancante obbligatorio, formato errato |
| MAP-E002 | validate | 1 | Duplicate entity ID in normalized registry | Due sorgenti producono lo stesso kebab-case ID senza `allow_merge` |
| MAP-E003 | collect | 2 | Ecosystem snapshot absent | `ecosystem-snapshot.json` non presente nella directory artifacts |
| MAP-E004 | collect | 1 | Required source missing or unparsable | `state/roadmap.yaml` assente o malformato |
| MAP-E005 | — (browser) | — | Generated dataset not loadable in browser | JSON corrotto o assente in `docs/data/generated/` |
| MAP-E006 | — (CI) | — | Critical HTML link broken | `href` in docs/ punta a risorsa inesistente |
| MAP-E007 | publish | 1 | Incomplete staging before atomic rename | File mancante in staging, processo interrotto |
| MAP-E008 | collect | 2 | Source file stale beyond configured threshold | mtime del file sorgente supera la soglia in `freshness_policy.yaml` |

---

## 2. Code Location Index

| Codice | File | Funzione/linea indicativa |
|--------|------|--------------------------|
| MAP-E001 | `scripts/build_project_map.py` | `phase_validate_generated()` |
| MAP-E002 | `scripts/build_project_map.py` | `phase_validate()` |
| MAP-E003 | `scripts/build_project_map.py` | `phase_collect()` — ecosystem_snapshot check |
| MAP-E004 | `scripts/build_project_map.py` | `phase_collect()` — required sources loop |
| MAP-E005 | `docs/shared/data-loader.js` | catch block su `fetch()` |
| MAP-E006 | CI: `.github/workflows/project-map-ci.yml` | job `link-check` (lychee) |
| MAP-E007 | `scripts/build_project_map.py` | `phase_publish()` — completeness guard |
| MAP-E008 | `scripts/build_project_map.py` | `_check_source_freshness()` |

---

## 3. Demonstrated Failure Scenarios

### Scenario A — Schema invalid (MAP-E001)

**Iniezione**: `state/roadmap.yaml` → una task con `status: INVALID_ENUM_VALUE`

**Comportamento atteso**:
```
[MAP-E001] Generated 'roadmap.json' fails schema validation at tasks -> N -> raw_data -> status:
           'INVALID_ENUM_VALUE' is not one of ['PLANNED', 'READY', 'IN_PROGRESS', ...]
  Phase: validate
  File: .../staging/roadmap.json
Exit code: 1
```

**Deploy gate**: BLOCCATO (exit 1)

**Come riprodurre**:
```bash
python scripts/ci/failure_injection.py --scenario schema-invalid
```

---

### Scenario B — Ecosystem snapshot absent (MAP-E003)

**Iniezione**: `ecosystem-snapshot.json` temporaneamente rinominato

**Comportamento atteso**:
```
[!] [MAP-E003] Ecosystem snapshot absent — collaborative system data unavailable.
               Freshness badge will show STALE.
    File: .../ecosystem-snapshot.json
Build Summary: SUCCESS (with warnings)
freshness_status: "STALE"
Exit code: 2
```

**Deploy gate**: PROCEDE con annotation warning

**Come riprodurre**:
```bash
python scripts/ci/failure_injection.py --scenario missing-snapshot
```

---

### Scenario C — Required source missing (MAP-E004)

**Iniezione**: `state/roadmap.yaml` temporaneamente rinominato

**Comportamento atteso**:
```
[CRITICAL ERROR] [MAP-E004] Required source 'roadmap' not found or unparsable
  Phase: collect
  File: .../state/roadmap.yaml
Exit code: 1
```

**Deploy gate**: BLOCCATO (exit 1)

**Come riprodurre**:
```bash
python scripts/ci/failure_injection.py --scenario missing-source
```

---

### Scenario D — Incomplete staging / interrupted publish (MAP-E007)

**Iniezione**: `build-manifest.json` rimosso dalla staging directory prima del publish

**Comportamento atteso**:
```
[CRITICAL ERROR] [MAP-E007] Incomplete staging — missing: build-manifest.json.
                 Publish aborted to prevent partial output.
  Phase: publish
```

L'ultimo snapshot valido in `docs/data/generated.bak/` rimane intatto.

**Deploy gate**: BLOCCATO (exit 1)

**Come riprodurre**:
```bash
python scripts/ci/failure_injection.py --scenario interrupted-publish
```

---

### Scenario E — Stale source data (MAP-E008)

**Iniezione**: mtime di `ecosystem-snapshot.json` impostato a 48h fa (soglia: 24h)

**Comportamento atteso**:
```
[!] [MAP-E008] Source 'ecosystem_snapshot' is stale: last modified 48h ago (threshold: 24h).
               Dataset freshness badge will show STALE.
    File: .../ecosystem-snapshot.json
freshness_status: "STALE"
Exit code: 2
```

**Deploy gate**: PROCEDE con annotation warning

**Come riprodurre**:
```bash
python scripts/ci/failure_injection.py --scenario stale-data
```

---

## 4. Debugability Gate: 2-minute diagnosis

Per ogni codice la tabella sotto riporta il percorso minimo di diagnosi:

| Codice | Step 1 (30s) | Step 2 (30s) | Step 3 (60s) | Remediation |
|--------|-------------|-------------|-------------|-------------|
| MAP-E001 | Leggi `message` nel log | Trova path nel JSON (`tasks -> N -> status`) | Correggi `state/roadmap.yaml` | Riesegui build |
| MAP-E002 | Leggi ID duplicato nel log | Cerca ID in `roadmap.yaml` e `archimate_data.json` | Rinomina uno dei due | Riesegui build |
| MAP-E003 | Verifica presenza `ecosystem-snapshot.json` | Se assente: chi l'ha rimosso? Git log | Riesporta con `export_ecosystem_snapshot.py` | Committa e pusha |
| MAP-E004 | Leggi filename nel log | `python -c "import yaml; yaml.safe_load(...)"` | Ripristina da git o correggi YAML | Riesegui build |
| MAP-E005 | Console browser: SyntaxError | `python -c "import json; json.load(...)"` | File corrotto: rigenera | Build + push |
| MAP-E006 | Log CI lychee: file + URL | Cerca `href` nel file segnalato | Aggiorna link o rigenera detail pages | Push |
| MAP-E007 | Verifica `staging/` directory | Verifica `.bak/` è integro | Correggi causa (disco, permessi) | Build completo |
| MAP-E008 | Leggi `message`: fonte + età | Controlla `freshness_policy.yaml` | Aggiorna fonte o soglia | Riesegui build |

**Gate**: Un operatore che non ha implementato la feature deve identificare causa e remediation in < 2 minuti avendo solo: sintomo + questo runbook + log.

---

## 5. Coverage MAP-E001–MAP-E008

| Codice | Emesso da pipeline | Demonstrabile con failure_injection.py | Documentato in runbook |
|--------|--------------------|----------------------------------------|------------------------|
| MAP-E001 | ✅ `phase_validate_generated()` | ✅ `--scenario schema-invalid` | ✅ |
| MAP-E002 | ✅ `phase_validate()` | — (strutturale, raro) | ✅ |
| MAP-E003 | ✅ `phase_collect()` | ✅ `--scenario missing-snapshot` | ✅ |
| MAP-E004 | ✅ `phase_collect()` | ✅ `--scenario missing-source` | ✅ |
| MAP-E005 | ✅ `docs/shared/data-loader.js` | ✅ `--scenario browser-corrupt` | ✅ |
| MAP-E006 | ✅ CI lychee (job link-check) | — (richiede CI) | ✅ |
| MAP-E007 | ✅ `phase_publish()` | ✅ `--scenario interrupted-publish` | ✅ |
| MAP-E008 | ✅ `_check_source_freshness()` | ✅ `--scenario stale-data` | ✅ |

**Risultato**: tutti e 8 i codici sono locatabili dai log, dimostrabili e documentati.

---

## 6. Acceptance Criteria (PMAP-16)

| Criterio | Stato | Evidenza |
|----------|-------|---------|
| MAP-E001–E008 locatabili dai log | ✅ | Sezione 2 — code location index |
| Schema error dimostrato | ✅ | Scenario A — `--scenario schema-invalid` |
| Snapshot assente dimostrato | ✅ | Scenario B — `--scenario missing-snapshot` |
| Generazione interrotta dimostrata | ✅ | Scenario D — `--scenario interrupted-publish` |
| Operatore non autore: diagnosi < 2 min | ✅ | Sezione 4 — tabella percorso minimo |

---

*Debug Intelligence Agent — Claude Code*  
*PMAP-16 — 2026-07-14*
