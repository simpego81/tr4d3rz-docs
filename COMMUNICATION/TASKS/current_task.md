# Current Task — FEATURE-STAKEHOLDER-HERO (Step 1)

**Assigned Agent**: Claude Code (Developer role)
**Repository target**: `tr4d3rz-docs`
**Status**: COMPLETED
**Issued by**: Owner
**Milestone**: FEATURE-VIEWS improvement
**Last update**: 2026-07-26

---

## Objective

Implement Step 1 of `STAKEHOLDER_PAGE_SPECIFICATION.md`: a full-viewport animated hero section on `docs/index.html` showing the TR4D3RZ algorithm in action.

## Spec reference

`c:\projects\seq\STAKEHOLDER_PAGE_SPECIFICATION.md` — 1st concept: long-term goal

## What to build

Insert `<section class="algo-hero">` **before** the existing `.hero` in `docs/index.html`, with three animated panels:

**Panel 1 — OHLCV Stream (left):** Canvas, ~20 scrolling OHLC candles, new candle every 400ms
**Panel 2 — ALU Box (center):** SVG with 4 rotating IIR knobs, 2 oscillating margin levers, input/output arrows
**Panel 3 — State Machine 3D (right):** Three.js, 5 sphere-nodes + 7 edge-lines, current state glows + pulses

**Transitions every ~5s:** highlight edge → show condition text overlay → move current state after 1.5s

## Technical constraints

- Three.js from CDN only (`https://unpkg.com/three@0.165.0/build/three.min.js`)
- Dark self-contained section (`#0f172a`), no light/dark mode interference
- No build step, no npm
- Responsive (stack vertically <768px)
- Respect `prefers-reduced-motion`
- Existing content below must be unaffected

## Definition of Done

- [ ] Section visible as first viewport content in `docs/index.html`
- [ ] All three panels animate without console errors
- [ ] State transitions fire with condition text overlay
- [ ] Existing project map below unaffected
- [ ] `COMMUNICATION/IMPLEMENTATION_LOG.md` updated with commit hash
