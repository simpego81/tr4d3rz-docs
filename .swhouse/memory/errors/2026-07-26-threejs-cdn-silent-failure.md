---
date: 2026-07-26
cycle: N/A
severity: high
---

## What failed

The Three.js state machine canvas in `docs/index.html` was completely blank after delivery. No JS error appeared in the console, no visual indicator showed failure.

## Root cause

Two compounding issues:

1. **Wrong CDN path**: `https://unpkg.com/three@0.165.0/build/three.min.js` does not serve a UMD global build for r165. `window.THREE` was undefined at runtime.

2. **Silent failure propagation**: `initSM()` checked `if (!T) return null` without any error output. The render loop handled null with `if (smFn) smFn.update(t)` — no error, no visible sign, just a blank canvas.

## How it was detected

Owner validated the feature visually in a browser and reported the canvas was blank. No automated check caught it before delivery.

## Resolution

- Replaced CDN URL with `https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js` (r128, verified UMD global)
- Added `onerror` on the `<script>` tag
- Added `console.error` in `initSM()` + DOM fallback message
- Added `try/catch` around `WebGLRenderer` constructor

## Lesson

**CDN script failures are silent by default.** A CDN returning 404, or serving an ES module instead of a UMD global, will simply leave `window.THREE` undefined. Dependent code that silently handles `undefined` dependencies will appear to work until someone opens the browser.

**Reusable pattern for future frontend tasks:**
- Pin CDN URLs to a known-working version+path combination (e.g., r128 from cdnjs for Three.js globals)
- Always add `onerror` to external `<script>` tags
- Always add `console.error` (not just `return null`) when a dependency is missing
- Add a visible fallback message so failures surface immediately
- Add a try/catch around WebGL/Canvas API constructors

## Process gap exposed

The TR4D3RZ Tester, Reviewer, and Developer agent protocols had no frontend verification rules. The Software House AI Scientist protocol listed no "browser observation" verification method. All fixed in the 2026-07-26 process update — see `software-house-ai/protocols/frontend-checklist.md`.
