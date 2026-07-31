---
date: 2026-07-30
cycle: "002"
title: UX principles for scroll-driven narratives in stakeholder presentations
domain: frontend / UX / storytelling
relates_to:
  - ".swhouse/memory/errors/2026-07-26-threejs-cdn-silent-failure.md"
  - ".swhouse/memory/errors/2026-07-30-ga-phases-disconnected-overlay.md"
  - ".swhouse/memory/decisions/2026-07-30-gh-pages-ga-2.5-2.8-correct-approach.md"
---

## Summary

Scroll-driven narratives for technical stakeholders (e.g., "how a Genetic Algorithm works") require strict visual continuity: each phase must visibly build on the previous one using the same DOM elements, not replace them. When a viewer sees a new, unrelated element appear, the cognitive thread breaks — they stop following the algorithm and start questioning the interface. This lesson was learned from Cycle #002 feedback, where separate overlay panels for GA phases 2.5–2.8 broke continuity with the table established in 2.3.

## Core principles

### 1. Persistent identity over replacement

Every named concept (individual, genome table, portfolio, CAGR list) must correspond to a single, persistent DOM element throughout the entire narrative. Phases animate the state of that element — they do not create structural replacements. If a new element is needed, the spec must explicitly say "a new X appears" (not just "an X is shown").

### 2. One source of truth per visual concept

Map concepts to DOM nodes at design time, before writing any animation code:

| Narrative concept | Single DOM node | Phases that use it |
|---|---|---|
| Genome/CAGR table | `#ga-table` | 2.3, 2.5, 2.6, 2.7 |
| Individual border card | `.individual-card` | 2.1, 2.4, 2.8 |
| Portfolio stack | `#portfolio-stack` | 2.4, 2.8 |

This map is the contract. No phase may instantiate an alternative node for a concept already in the map.

### 3. Styling additions are never creative additions

Unspecified visual embellishments (color-coding, gradient fills, animated borders) are bugs unless the spec calls for them. For technical stakeholder presentations, clarity of data always outweighs visual richness. Plain text, standard weights, and a single accent color for highlights produce more legible and trustworthy results than decorative schemes.

### 4. Scroll trigger architecture: pin → transform → unpin

For multi-phase narratives using GSAP ScrollTrigger:
- Pin a single container (e.g., `#ga-stage`) for the entire concept
- Each phase is a labeled sub-timeline within the main scrub timeline
- State changes (row count, row visibility, cell highlighting) are driven by timeline position, not by separate scroll triggers per phase
- This prevents phase desynchronization when the user scrolls at irregular speed

### 5. Pre-generate, then reveal

All data (genome rows, CAGR values, arrow positions) must be generated at `init()` time and hidden (opacity: 0 or display: none). Phases only reveal and animate pre-existing content — they never create DOM nodes mid-scroll. This ensures scroll-back fidelity and prevents layout reflow during animation.

### 6. Validate with a human eye before delivery

Automated tests cannot catch visual narrative discontinuity. The SCIENTIST role must open the page in a real browser, scroll slowly through every phase, and explicitly verify: "Is this the same element I saw in the previous phase?" before the delivery gate is passed. This check must be listed as a mandatory step in the Scientist protocol for any scroll-driven narrative task.

## Anti-patterns to avoid

| Anti-pattern | Why it fails |
|---|---|
| New overlay element per phase | Breaks visual identity; viewer loses the thread |
| Color-coding not in spec | Adds cognitive load; coloring implies meaning that may not exist |
| Phase-specific scroll triggers | Desynchronization on non-linear scrolling |
| DOM node creation mid-scroll | Layout reflow causes jank; scroll-back shows incomplete state |
| `return null` without `console.error` | Silent failures impossible to debug (see CDN error, 2026-07-26) |

## Rule for future agents

When tasked with implementing a scroll-driven narrative phase, read the previous phase's implementation first, identify every visible DOM element by ID, and confirm that your new phase either TRANSFORMS an existing element or EXPLICITLY introduces a new one per spec — then write the animation code.
