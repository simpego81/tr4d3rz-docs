---
date: 2026-07-30
cycle: "002"
severity: high
component: docs/index.html (GitHub Pages — 2nd Concept GA phases)
reported_by: owner
---

## What failed

Phases 2.5 (Selection), 2.6 (Crossover), and 2.7 (Mutation) of the 2nd Concept scroll-driven narrative were implemented as entirely separate full-screen overlay elements (`#ga-sel`, `#ga-xover`, `#ga-mut`) with newly generated HTML tables and colored genome-block strips. These were disconnected from the data table already rendered in phases 2.1–2.4, which contained the actual genome strings and CAGR values.

## Root cause

The BUILDER agent read the spec requirements for each phase in isolation and created independent DOM structures for each transition. The spec stated "la tabella prende tutta la visuale" (the table takes up the full view) — meaning the existing table should EXPAND, not be REPLACED. This continuity constraint was not identified as a cross-phase dependency. The CRITIC and REVIEWER agents did not check visual narrative continuity against the table established in 2.3 before marking the feature ready for delivery.

Two compounding sub-errors:
1. **Identity break**: The table in 2.5+ used colored genome-block strips. The spec never mentions color-coding. Coloring was an unsolicited creative addition that contradicted the spec's implicit requirement of a plain data table.
2. **Process gap**: No agent role had an explicit checklist item for "is this UI element the same element as shown in the previous phase?" — only functional correctness was reviewed.

## How it was detected

Owner validated the feature in the browser and reported the mismatch verbatim: "la tabella deve essere la stessa dei passi precedenti, quella che contiene i genoma e i cagr. Non devono essere colorate."

## Lesson

**Scroll-driven narrative phases share state — DOM elements introduced in one phase must persist and transform, not be replaced.** When a spec says a UI element "takes up the full view", "expands", or "moves", it means the SAME element changes — new elements are never the answer. Unspecified creative additions (e.g., colored genome strips) are bugs, not features: add only what the spec requires.

## Rule for future agents

When implementing a multi-phase scroll animation, map every visual element to a single source DOM node and annotate which phases READ vs TRANSFORM that node; never instantiate a parallel replacement element for an element already in the DOM.

## Process gap exposed

The Software House AI cycle lacked an explicit cross-phase visual continuity check in the CRITIC and REVIEWER protocols. A "visual continuity audit" step must be added: for each new phase, verify that every displayed UI element either (a) is the same DOM node as in the previous phase, or (b) is explicitly introduced as NEW in the spec.

See also: `.swhouse/memory/errors/2026-07-26-threejs-cdn-silent-failure.md` — same cycle, complementary frontend process gap.
