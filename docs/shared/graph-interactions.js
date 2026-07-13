/**
 * TR4D3RZ Project Map — Graph Interactions
 *
 * Shared D3 interaction modules used by all four map pages.
 * Requires D3 v7+ loaded before this script.
 *
 * Modules:
 *   setupZoom(svg, group, opts)      — zoom + pan + reset
 *   createTooltip(parent)            — accessible floating tooltip
 *   createFocusManager(opts)         — node focus + neighbor highlight
 *   setupKeyboardNav(opts)           — arrow-key graph traversal
 *   bindDeepLink(opts)               — URL hash ↔ selected node
 *   applySearchFilter(opts)          — real-time node/link filter
 */

const GraphInteractions = (() => {
  'use strict';

  /* ------------------------------------------------------------------ */
  /* Helpers                                                              */
  /* ------------------------------------------------------------------ */

  function prefersReducedMotion() {
    return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  }

  function clamp(value, min, max) {
    return Math.max(min, Math.min(max, value));
  }

  /* ------------------------------------------------------------------ */
  /* Zoom / Pan                                                           */
  /* ------------------------------------------------------------------ */

  /**
   * Attach D3 zoom behaviour to an SVG.
   *
   * @param {d3.Selection} svg      — the <svg> element selection
   * @param {d3.Selection} group    — inner <g> that receives the transform
   * @param {object}       [opts]
   * @param {number}       [opts.scaleMin=0.25]
   * @param {number}       [opts.scaleMax=4]
   * @param {Function}     [opts.onZoom]          — callback(transform)
   * @param {HTMLElement}  [opts.resetButton]     — button that resets view
   * @returns {{ zoom: d3.ZoomBehavior, resetView: Function }}
   */
  function setupZoom(svg, group, opts = {}) {
    const {
      scaleMin = 0.25,
      scaleMax = 4,
      onZoom = null,
      resetButton = null,
    } = opts;

    const duration = prefersReducedMotion() ? 0 : 300;

    const zoom = d3.zoom()
      .scaleExtent([scaleMin, scaleMax])
      .on('zoom', (event) => {
        group.attr('transform', event.transform);
        if (onZoom) onZoom(event.transform);
      });

    svg.call(zoom);

    /* Disable double-click zoom (use explicit reset instead) */
    svg.on('dblclick.zoom', null);

    function resetView() {
      svg.transition().duration(duration).call(zoom.transform, d3.zoomIdentity);
    }

    /* Keyboard: + / - / 0 while SVG is focused */
    svg.on('keydown.zoom', (event) => {
      if (event.key === '+' || event.key === '=') {
        event.preventDefault();
        svg.transition().duration(duration).call(zoom.scaleBy, 1.3);
      } else if (event.key === '-') {
        event.preventDefault();
        svg.transition().duration(duration).call(zoom.scaleBy, 1 / 1.3);
      } else if (event.key === '0') {
        event.preventDefault();
        resetView();
      }
    });

    if (resetButton) {
      resetButton.addEventListener('click', resetView);
    }

    return { zoom, resetView };
  }

  /* ------------------------------------------------------------------ */
  /* Tooltip                                                              */
  /* ------------------------------------------------------------------ */

  /**
   * Create an accessible floating tooltip.
   *
   * Announce content changes via aria-live so screen readers pick them up.
   *
   * @param {HTMLElement} parent — element to append the tooltip to
   * @returns {{ show: Function, hide: Function, move: Function }}
   */
  function createTooltip(parent = document.body) {
    const el = document.createElement('div');
    el.className = 'graph-tooltip';
    el.setAttribute('role', 'tooltip');
    el.setAttribute('aria-live', 'polite');
    el.setAttribute('aria-atomic', 'true');
    el.style.display = 'none';
    parent.appendChild(el);

    /* Live region (offscreen) for screen readers — separate from visual */
    const live = document.createElement('div');
    live.setAttribute('aria-live', 'polite');
    live.setAttribute('aria-atomic', 'true');
    live.className = 'visually-hidden';
    parent.appendChild(live);

    function show(html, x, y) {
      el.innerHTML = html;
      el.style.display = 'block';
      _position(x, y);
      live.textContent = el.textContent.trim();
    }

    function hide() {
      el.style.display = 'none';
      live.textContent = '';
    }

    function move(x, y) {
      if (el.style.display !== 'none') _position(x, y);
    }

    function _position(x, y) {
      const pad = 12;
      const rect = el.getBoundingClientRect();
      const vw = window.innerWidth;
      const vh = window.innerHeight;

      let left = x + pad;
      let top  = y + pad;

      /* Flip left if tooltip overflows right edge */
      if (left + rect.width > vw - pad) left = x - rect.width - pad;
      /* Flip up if tooltip overflows bottom edge */
      if (top + rect.height > vh - pad) top = y - rect.height - pad;

      el.style.left = `${clamp(left, pad, vw - rect.width - pad)}px`;
      el.style.top  = `${clamp(top,  pad, vh - rect.height - pad)}px`;
    }

    return { show, hide, move };
  }

  /* ------------------------------------------------------------------ */
  /* Focus / Highlight                                                    */
  /* ------------------------------------------------------------------ */

  /**
   * Manage node focus and neighbour highlighting.
   *
   * @param {object} opts
   * @param {d3.Selection} opts.nodeSelection   — D3 selection of node elements
   * @param {d3.Selection} opts.linkSelection   — D3 selection of link elements
   * @param {Function}     opts.getNodeId       — (d) => string
   * @param {Function}     opts.getSourceId     — (link) => string
   * @param {Function}     opts.getTargetId     — (link) => string
   * @param {string}       [opts.dimClass='dim']
   * @param {string}       [opts.highlightClass='highlighted']
   * @returns {{ focus: Function, clear: Function, focusedId: Function }}
   */
  function createFocusManager(opts) {
    const {
      nodeSelection,
      linkSelection,
      getNodeId,
      getSourceId,
      getTargetId,
      dimClass = 'dim',
      highlightClass = 'highlighted',
    } = opts;

    let _focusedId = null;

    function focus(datum) {
      const id = getNodeId(datum);
      _focusedId = id;

      /* Find neighbour IDs */
      const neighbours = new Set([id]);
      linkSelection.each(d => {
        const src = getSourceId(d);
        const tgt = getTargetId(d);
        if (src === id) neighbours.add(tgt);
        if (tgt === id) neighbours.add(src);
      });

      /* Dim/highlight nodes */
      nodeSelection
        .classed(dimClass, d => !neighbours.has(getNodeId(d)))
        .classed(highlightClass, d => getNodeId(d) === id);

      /* Dim links */
      linkSelection.classed(dimClass, d =>
        getSourceId(d) !== id && getTargetId(d) !== id
      );
    }

    function clear() {
      _focusedId = null;
      nodeSelection.classed(dimClass, false).classed(highlightClass, false);
      linkSelection.classed(dimClass, false);
    }

    function focusedId() { return _focusedId; }

    return { focus, clear, focusedId };
  }

  /* ------------------------------------------------------------------ */
  /* Keyboard Navigation                                                  */
  /* ------------------------------------------------------------------ */

  /**
   * Enable arrow-key traversal between graph nodes.
   *
   * Nodes must be rendered as <g> elements with tabindex="0" and
   * a data attribute [data-node-id].
   *
   * @param {object}       opts
   * @param {SVGElement}   opts.svgElement
   * @param {Function}     opts.getNodes      — () => datum[]
   * @param {Function}     opts.getNodeId     — (datum) => string
   * @param {Function}     opts.getNodePos    — (datum) => {x, y}
   * @param {Function}     [opts.onSelect]    — (datum) => void
   * @param {Function}     [opts.onActivate]  — (datum) => void  (Enter/Space)
   */
  function setupKeyboardNav(opts) {
    const {
      svgElement,
      getNodes,
      getNodeId,
      getNodePos,
      onSelect = () => {},
      onActivate = () => {},
    } = opts;

    let _currentId = null;

    svgElement.addEventListener('keydown', (event) => {
      const nodes = getNodes();
      if (!nodes.length) return;

      const key = event.key;
      if (!['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'Enter', ' '].includes(key)) return;

      event.preventDefault();

      /* Find current datum */
      const current = nodes.find(d => getNodeId(d) === _currentId) || nodes[0];
      const pos = getNodePos(current);

      if (key === 'Enter' || key === ' ') {
        onActivate(current);
        return;
      }

      /* Choose nearest node in direction */
      const dx = key === 'ArrowRight' ? 1 : key === 'ArrowLeft' ? -1 : 0;
      const dy = key === 'ArrowDown'  ? 1 : key === 'ArrowUp'   ? -1 : 0;

      let bestNode = null;
      let bestScore = Infinity;

      for (const d of nodes) {
        if (getNodeId(d) === getNodeId(current)) continue;
        const p = getNodePos(d);
        const relX = p.x - pos.x;
        const relY = p.y - pos.y;

        /* Project onto direction vector */
        const dot = relX * dx + relY * dy;
        if (dot <= 0) continue;

        /* Penalise lateral offset */
        const perp = Math.abs(relX * dy - relY * dx);
        const score = dot + perp * 2;

        if (score < bestScore) {
          bestScore = score;
          bestNode = d;
        }
      }

      const next = bestNode || current;
      _currentId = getNodeId(next);
      onSelect(next);

      /* Move DOM focus to the node element */
      const el = svgElement.querySelector(`[data-node-id="${CSS.escape(_currentId)}"]`);
      if (el) el.focus();
    });

    /* Track focus from pointer interactions */
    function setFocus(id) { _currentId = id; }

    return { setFocus };
  }

  /* ------------------------------------------------------------------ */
  /* Deep Link                                                            */
  /* ------------------------------------------------------------------ */

  /**
   * Synchronise selected node with URL hash (#node-id).
   *
   * @param {object}   opts
   * @param {Function} opts.getSelectedId   — () => string|null
   * @param {Function} opts.selectById      — (id: string) => void
   * @param {Function} opts.clearSelection  — () => void
   */
  function bindDeepLink(opts) {
    const { getSelectedId, selectById, clearSelection } = opts;

    /* Restore from URL on load */
    function restore() {
      const hash = window.location.hash.slice(1);
      if (hash) selectById(decodeURIComponent(hash));
    }

    /* Update URL when selection changes (call this from your select handler) */
    function update() {
      const id = getSelectedId();
      const newHash = id ? `#${encodeURIComponent(id)}` : '';
      if (window.location.hash !== newHash) {
        history.replaceState(null, '', newHash || window.location.pathname + window.location.search);
      }
    }

    window.addEventListener('hashchange', () => {
      const hash = window.location.hash.slice(1);
      if (hash) selectById(decodeURIComponent(hash));
      else clearSelection();
    });

    return { restore, update };
  }

  /* ------------------------------------------------------------------ */
  /* Search / Filter                                                      */
  /* ------------------------------------------------------------------ */

  /**
   * Filter graph nodes and links based on a search term and category.
   *
   * @param {object}       opts
   * @param {d3.Selection} opts.nodeSelection
   * @param {d3.Selection} opts.linkSelection
   * @param {Function}     opts.getNodeText    — (d) => string  (searchable text)
   * @param {Function}     opts.getNodeCat     — (d) => string  (category/status)
   * @param {Function}     opts.getSourceId
   * @param {Function}     opts.getTargetId
   * @param {Function}     opts.getNodeId
   * @param {string}       [opts.hiddenClass='filtered-out']
   * @returns {{ apply: Function, reset: Function }}
   */
  function applySearchFilter(opts) {
    const {
      nodeSelection,
      linkSelection,
      getNodeText,
      getNodeCat,
      getSourceId,
      getTargetId,
      getNodeId,
      hiddenClass = 'filtered-out',
    } = opts;

    function apply(term = '', category = '') {
      const q = term.trim().toLowerCase();

      const visibleIds = new Set();

      nodeSelection.each(d => {
        const matchText = !q || getNodeText(d).toLowerCase().includes(q);
        const matchCat  = !category || getNodeCat(d) === category;
        if (matchText && matchCat) visibleIds.add(getNodeId(d));
      });

      nodeSelection.classed(hiddenClass, d => !visibleIds.has(getNodeId(d)));
      linkSelection.classed(hiddenClass, d =>
        !visibleIds.has(getSourceId(d)) || !visibleIds.has(getTargetId(d))
      );

      return visibleIds.size;
    }

    function reset() {
      nodeSelection.classed(hiddenClass, false);
      linkSelection.classed(hiddenClass, false);
    }

    return { apply, reset };
  }

  /* ------------------------------------------------------------------ */
  /* Public API                                                           */
  /* ------------------------------------------------------------------ */

  return {
    setupZoom,
    createTooltip,
    createFocusManager,
    setupKeyboardNav,
    bindDeepLink,
    applySearchFilter,
  };
})();
