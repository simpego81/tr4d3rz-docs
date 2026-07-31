# TR4D3RZ — META CONVERGENCE METRICS

**Maintainer**: Claude Code (Primary Agent, ruolo Meta-Optimizer)  
**Last update**: 2026-07-15  
**Status**: ACTIVE

---

## Scopo

Traccia le metriche di qualità della convergenza del sistema AI. Usato da Claude Code in modalità Meta-Optimizer per rilevare inefficienze sistemiche.

**Core Question**: Il sistema converge verso la soluzione giusta abbastanza velocemente?

---

## 1. Requirement Churn

**Definizione**: frequenza di revisioni delle spec per feature.  
**Soglia**: >3 revisioni indica instabilità dei requisiti.

| Feature | Revisioni spec | Status | Ultima modifica |
|---|---|---|---|
| M1-T1 | 1 | COMPLETED | 2026-06-05 |
| M1-T2 | 2 | COMPLETED | 2026-06-05 |
| M1-T2-B | 3 | COMPLETED | 2026-06-14 |
| M1-T3 | 1 | IN_PROGRESS | 2026-07-15 |
| M1-T4 | 1 | PENDING | — |
| M1-T5 | 1 | PENDING | — |
| FEATURE-DOCS-PROJECT-MAP | 2 | FUNCTIONALLY COMPLETE | 2026-07-14 |

**Assessment**: GOOD — churn basso, spec stabili.

---

## 2. Rework Ratio

**Definizione**: `reworked_lines / total_lines` — churn di codice per feature.  
**Soglia**: >0.4 indica iterazioni inefficienti.

| Feature | Linee totali | Linee rework | Ratio | Status |
|---|---|---|---|---|
| M1-T1 | ~500 | ~150 | 0.30 | ACCEPTABLE |
| M1-T2 | ~700 | ~200 | 0.29 | GOOD |
| M1-T2-B | ~200 | ~80 | 0.40 | BORDERLINE |
| M1-T3 (lib) | ~400 | TBD | — | IN_PROGRESS |

**Assessment**: ACCEPTABLE — M1-T2-B borderline ma entro tolleranza.

---

## 3. Review Cycle Count

**Definizione**: numero di loop di review prima dell'accettazione.  
**Soglia**: >2 cicli indica qualità iniziale scarsa o criteri di accettazione poco chiari.

| Feature | Cicli review | Status | Note |
|---|---|---|---|
| M1-T1 | 1 | COMPLETED | Accettazione clean |
| M1-T2 | 1 | COMPLETED | Accettazione clean |
| M1-T2-B | 2 | COMPLETED | Refinamento error handling |
| M1-T3 | TBD | IN_PROGRESS | — |

**Assessment**: GOOD — convergenza entro 1-2 cicli.

---

## 4. Demo Validation Time

**Definizione**: tempo (min) per l'owner per validare una feature via demo.  
**Soglia**: >15 min indica scarsa osservabilità o demo complessa.

| Feature | Tempo (min) | Status |
|---|---|---|
| M1-T2 | ~10 | COMPLETED |
| M1-T2-B | ~5 | COMPLETED |
| FEATURE-DOCS-PROJECT-MAP | ~8 (automatico) | PARTIAL (browser gate manuale) |
| M1-T3 | TBD | IN_PROGRESS |

**Assessment**: GOOD — validazione rapida.

---

## 5. Inefficienze sistemiche rilevate

### 2026-07-30 — Cycle #002: GA phases 2.5–2.8 visual continuity failure

**Trigger**: Owner rejected delivery of GitHub Pages 2nd Concept GA phases 2.5–2.8 (selection, crossover, mutation).

**Problema rilevato**: BUILDER created independent full-screen overlay DOM elements for phases 2.5–2.8 instead of transforming the existing table from 2.3. Added unsolicited colored genome-block strips not present in spec. CRITIC and REVIEWER did not catch the identity break before delivery. Review cycle count for this feature went to 2 (borderline threshold).

**Intervento**:
- Documented error pattern: `.swhouse/memory/errors/2026-07-30-ga-phases-disconnected-overlay.md`
- Documented correct approach: `.swhouse/memory/decisions/2026-07-30-gh-pages-ga-2.5-2.8-correct-approach.md`
- Documented UX knowledge: `.swhouse/memory/knowledge/2026-07-30-scroll-driven-narrative-ux.md`
- Required process fix: CRITIC/REVIEWER protocol must add "visual continuity audit" step for multi-phase scroll narratives (verify each phase transforms existing DOM nodes per spec)
- Required process fix: SCIENTIST protocol must add mandatory browser observation of scroll narrative before delivery gate

**Impatto atteso**: no future phase-replacement errors in scroll-driven narrative implementations.

---

### 2026-07-15 — Ristrutturazione modello agenti

**Trigger**: utente ha rimosso tutti gli agenti esterni (Manus, Copilot, Antigravity, HRA).

**Problema rilevato**: stato dei file di coordinamento era cronicamente stale. File di stato inconsistenti con la realtà del codice (es. persistence IMPLEMENTATION_LOG = NOT_STARTED ma codice esistente). Sessione di ripresa richiedeva >10 min di diagnosi.

**Intervento**:
- Rimossi tutti i riferimenti agli agenti esterni
- Nuovo modello: Claude Code (primary) + subagent interni
- Aggiornati: AGENTS.md, SUBAGENT_PROTOCOL.md, DASHBOARD.md, project_state.md, current_task.md files
- Aggiunto SUBAGENT_PROTOCOL.md come guida operativa per orchestrazione

**Impatto atteso**: session resumption <5 min; stato file sincronizzato con realtà.

### 2026-06-19 — Baseline

**Assessment**: ecosistema convergeva bene. Nessuna inefficienza critica.

---

## 6. Convergence Velocity

**Metrica**: task completati per settimana.

| Periodo | Task completati | Velocity |
|---|---|---|
| 2026-06-05 → 2026-07-10 | 4 (T0..T2-B) | ~1.1 task/settimana |
| 2026-07-10 → 2026-07-15 | 0 (lavoro documentale) | 0 (non conta come task tecnico) |

**Prossima review**: dopo completamento M1-T3.

---

## 7. Trigger per review immediata

- >5 task COMPLETED senza commit git
- Churn >3 per qualsiasi task
- Rework ratio >0.5
- Demo validation time >20 min
- Owner segnala inefficienza ecosistema

---

*Maintainer: Claude Code (Meta-Optimizer role) — Aggiornato: 2026-07-15*
