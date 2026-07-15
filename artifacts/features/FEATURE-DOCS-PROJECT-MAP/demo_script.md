# Demo Script — FEATURE-DOCS-PROJECT-MAP

**Feature**: GitHub Pages Progressive Project Map  
**Demo ID**: DEMO-003-PMAP  
**Versione**: 1.0.0  
**Data**: 2026-07-14  
**Autore**: Implementation Agent (Claude Code)  
**Status**: READY

---

## Prerequisiti

```bash
# La demo gira su GitHub Pages (no server locale richiesto)
# URL: https://simpego81.github.io/tr4d3rz-docs/
# O in locale: aprire docs/index.html nel browser (Chrome/Firefox/Safari recente)

# Per i scenari di failure injection:
cd C:/projects/seq/tr4d3rz-docs
pip install pyyaml jsonschema
python scripts/ci/failure_injection.py --list
```

---

## Scenario D-PMAP-01 — Navigazione stakeholder (homepage mobile-first)

**Obiettivo**: L'utente stakeholder accede al progetto da smartphone e capisce lo stato in 60 secondi.

**Passi**:
1. Aprire `docs/index-new.html` (o https://simpego81.github.io/tr4d3rz-docs/index-new.html)
2. Impostare viewport a 390px (Chrome DevTools → iPhone 14 Pro)
3. Osservare la **metrics bar** in alto: milestones, task completati, task bloccati
4. Scorrere verso le **4 card** (Roadmap, Conceptual, Physical, Agents)
5. Verificare che nessun grafo pesante sia caricato (solo summary card)
6. Osservare la **freshness strip** in basso

**Osservabili attesi**:
- Layout usabile a 390px senza overflow orizzontale
- Metriche live caricate da `data/generated/roadmap.json`
- Freshness badge visibile (FRESH o STALE con motivo)
- Ogni card porta alla propria mappa con un tap

**Fallback se dataset assente**: contenuto statico con link navigabili e valori di default.

---

## Scenario D-PMAP-02 — Drill-down tecnico (quattro mappe)

**Obiettivo**: Un tecnico esplora ogni mappa e raggiunge il dettaglio di un nodo.

**Passi per ogni mappa**:

### Roadmap map (`maps/roadmap.html`)
1. Aprire la pagina
2. Nella timeline a sinistra, cliccare su **M1 — Foundational Backbone**
3. Nel grafo di destra, il nodo M1 si evidenzia
4. Cliccare su un task (es. M1-T3 Event Persistence)
5. Aprire la detail page → verificare: status, health, owners, dipendenze, blockers, evidence, source_refs

### Conceptual map (`maps/conceptual.html`)
1. Aprire la pagina
2. Cercare "MQTT" nel filtro
3. Cliccare sul nodo → detail page con concetti logici (no device fisici)

### Physical map (`maps/physical.html`)
1. Aprire la pagina
2. Individuare il nodo Raspberry Pi 2
3. Verificare cross-link ai concetti logici implementati

### Agents map (`maps/agents.html`)
1. Aprire la pagina
2. Toggle **Vista ruoli/autorità** vs **Vista flussi/handoff**
3. Verificare che HRA, veto gates e board siano visibili
4. Verificare che nessun campo riservato (.ecosystem) sia esposto

**Osservabili attesi**:
- Breadcrumb e back-link funzionanti
- status, health, owners, dependencies, blockers, updated_at, evidence, source_refs presenti
- Valori mancanti espliciti ("—") non omessi silenziosamente

---

## Scenario D-PMAP-03 — Aggiornamento SSOT e rigenerazione

**Obiettivo**: Una modifica alla roadmap si propaga nei dataset generati.

**Passi**:
```bash
# 1. Modifica controllata: aggiunge un campo evidence a un task
vim state/roadmap.yaml   # oppure usa editor preferito
# Aggiungere una entry evidence a M1-T3

# 2. Rigenera
python scripts/build_project_map.py --verbose

# 3. Osserva il manifest
cat docs/data/generated/build-manifest.json | python -m json.tool | grep -A3 '"generated_at"'
```

**Osservabili attesi**:
- `generated_at` aggiornato
- `sources[*].hash` del roadmap.yaml cambiato
- Conteggio entity invariato (solo evidence cambiata, non struttura)
- Build: SUCCESS, 0 errori, warnings stabili

---

## Scenario D-PMAP-04 — Roadmap senza date

**Obiettivo**: Verificare che milestone non datate non abbiano date stimate o inventate.

**Passi**:
1. Aprire `maps/roadmap.html`
2. Scorrere fino a M2, M3, M4, M5 (non datate)
3. Verificare che siano nella **corsia "non pianificata"** (not scheduled)
4. Aprire detail page di M2 → `start_date: null`, `end_date: null`

**Osservabili attesi**:
- Nessuna data stimata o interpolata
- Label "Non pianificata / Not scheduled" esplicita
- `actual_completion_date: null` per task futuri

---

## Scenario D-PMAP-05 — Snapshot collaborativo assente (MAP-E003)

**Obiettivo**: Dimostrare che la build continua (exit 2) con badge STALE quando il snapshot è assente.

**Passi**:
```bash
python scripts/ci/failure_injection.py --scenario missing-snapshot
```

**Osservabili attesi nel log**:
```
[!] [MAP-E003] Ecosystem snapshot absent — collaborative system data unavailable.
               Freshness badge will show STALE.
Build Summary: SUCCESS (with warnings)
freshness_status: "STALE"
Exit code: 2
```

**Note**: Il ripristino automatico avviene dopo la demo.

---

## Scenario D-PMAP-06 — Schema invalido (MAP-E001)

**Obiettivo**: Dimostrare che un enum non valido in roadmap.yaml blocca il publish.

**Passi**:
```bash
python scripts/ci/failure_injection.py --scenario schema-invalid
```

**Osservabili attesi nel log**:
```
[MAP-E001] Generated 'roadmap.json' fails schema validation
Exit code: 1
```

**Deploy gate**: BLOCCATO — nessun file scritto in `docs/data/generated/`.

---

## Scenario D-PMAP-07 — Generazione parziale interrotta (MAP-E007)

**Obiettivo**: Dimostrare che lo staging incompleto non produce output parziale.

**Passi**:
```bash
python scripts/ci/failure_injection.py --scenario interrupted-publish
```

**Osservabili attesi**:
```
[MAP-E007] Incomplete staging — missing: build-manifest.json.
           Publish aborted to prevent partial output.
Exit code: 1
```

**Backup**: `docs/data/generated.bak/` rimane integro e consultabile.

---

## Scenario D-PMAP-08 — Navigazione legacy (device matrix)

**Obiettivo**: Verificare che la vecchia homepage e le pagine device siano raggiungibili.

**Passi**:
1. Aprire `docs/device-matrix.html`
2. Cliccare su ogni card device (ESP, RPi2, STM32, Browser, etc.)
3. Verificare che ogni pagina device si apra (es. `docs/rasp2.html`)
4. Aprire `docs/holistic_view.html`

**Osservabili attesi**:
- Nessuna pagina orfana o 404
- Le pagine device esistenti restano funzionanti
- Il link alla nuova Project Map è visibile nella navigazione

---

## Verifica automatizzata (non richiede browser)

```bash
# Schema validation
python scripts/ci/validate_schemas.py

# Build pipeline
python scripts/build_project_map.py --verbose

# Failure injection (tutti e 6 gli scenari)
for SCENARIO in schema-invalid missing-snapshot missing-source browser-corrupt stale-data interrupted-publish; do
    echo "=== $SCENARIO ==="
    python scripts/ci/failure_injection.py --scenario $SCENARIO
done
```

---

## Checklist demo completa

| Scenario | Tipo | Evidenza |
|----------|------|---------|
| D-PMAP-01 | Browser | Screenshot homepage 390px |
| D-PMAP-02 | Browser | Screenshot drill-down da ognuna delle 4 mappe |
| D-PMAP-03 | CLI | Log build post-modifica SSOT |
| D-PMAP-04 | Browser | Screenshot roadmap milestone non datata |
| D-PMAP-05 | CLI ✅ | Output failure_injection.py |
| D-PMAP-06 | CLI ✅ | Output failure_injection.py |
| D-PMAP-07 | CLI ✅ | Output failure_injection.py |
| D-PMAP-08 | Browser | Screenshot device-matrix.html |

**Status automatizzati**: D-PMAP-05, D-PMAP-06, D-PMAP-07 sono reproducibili con un comando senza browser.  
**Status browser**: D-PMAP-01, D-PMAP-02, D-PMAP-03, D-PMAP-04, D-PMAP-08 richiedono verifica umana.
