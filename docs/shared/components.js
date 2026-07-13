/**
 * TR4D3RZ Project Map — Shared UI Components
 *
 * Reusable components used by all four map pages and the homepage.
 * Vanilla JS only — no framework required.
 *
 * Components:
 *   renderLegend(container, items)
 *   renderFilterPanel(container, opts)
 *   renderTextualFallback(container, entities, columns)
 *   renderViewportWarning(container, opts)
 *   renderFreshnessStrip(container, manifest)
 *   renderHealthBadge(status)        — returns HTML string
 *   renderStatusBadge(status)        — returns HTML string
 */

const Components = (() => {
  'use strict';

  /* ------------------------------------------------------------------ */
  /* Helpers                                                              */
  /* ------------------------------------------------------------------ */

  function esc(s) {
    return String(s ?? '')
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  /* ------------------------------------------------------------------ */
  /* Badges                                                               */
  /* ------------------------------------------------------------------ */

  const STATUS_LABELS = {
    PLANNED:     'Planned',
    READY:       'Ready',
    IN_PROGRESS: 'In Progress',
    COMPLETED:   'Completed',
    BLOCKED:     'Blocked',
    DEPRECATED:  'Deprecated',
    UNKNOWN:     'Unknown',
  };

  const HEALTH_LABELS = {
    HEALTHY: 'Healthy',
    AT_RISK: 'At Risk',
    BLOCKED: 'Blocked',
    STALE:   'Stale',
    UNKNOWN: 'Unknown',
  };

  /**
   * Return an HTML string for a status badge.
   * @param {string} status
   * @returns {string}
   */
  function renderStatusBadge(status) {
    const key = (status || 'UNKNOWN').toUpperCase();
    const cls = `badge badge-status-${key.toLowerCase().replace(/_/g, '-')}`;
    const label = STATUS_LABELS[key] || key;
    return `<span class="${esc(cls)}" aria-label="Status: ${esc(label)}">${esc(label)}</span>`;
  }

  /**
   * Return an HTML string for a health badge.
   * @param {string} health
   * @returns {string}
   */
  function renderHealthBadge(health) {
    const key = (health || 'UNKNOWN').toUpperCase();
    const cls = `badge badge-health-${key.toLowerCase().replace(/_/g, '-')}`;
    const label = HEALTH_LABELS[key] || key;
    return `<span class="${esc(cls)}" aria-label="Health: ${esc(label)}">${esc(label)}</span>`;
  }

  /* ------------------------------------------------------------------ */
  /* Legend                                                               */
  /* ------------------------------------------------------------------ */

  /**
   * Render a colour legend into a container element.
   *
   * @param {HTMLElement} container
   * @param {Array<{label: string, cssClass: string, description?: string}>} items
   */
  function renderLegend(container, items) {
    const ul = document.createElement('ul');
    ul.className = 'legend';
    ul.setAttribute('role', 'list');
    ul.setAttribute('aria-label', 'Legend');

    for (const item of items) {
      const li = document.createElement('li');
      li.className = 'legend-item';

      const swatch = document.createElement('span');
      swatch.className = `legend-swatch ${esc(item.cssClass)}`;
      swatch.setAttribute('aria-hidden', 'true');

      const text = document.createElement('span');
      text.className = 'legend-label';
      text.textContent = item.label;

      if (item.description) {
        li.title = item.description;
        li.setAttribute('aria-description', item.description);
      }

      li.appendChild(swatch);
      li.appendChild(text);
      ul.appendChild(li);
    }

    container.innerHTML = '';
    container.appendChild(ul);
  }

  /* ------------------------------------------------------------------ */
  /* Filter Panel                                                         */
  /* ------------------------------------------------------------------ */

  /**
   * Render a search + optional category filter panel.
   *
   * @param {HTMLElement} container
   * @param {object}      opts
   * @param {string}      [opts.searchPlaceholder='Search…']
   * @param {Array<{value:string, label:string}>} [opts.categories=[]]
   * @param {Function}    opts.onChange — ({term, category}) => void
   * @returns {{ reset: Function, setValue: Function }}
   */
  function renderFilterPanel(container, opts = {}) {
    const {
      searchPlaceholder = 'Search…',
      categories = [],
      onChange = () => {},
    } = opts;

    let _term = '';
    let _category = '';

    container.innerHTML = `
      <div class="filter-panel" role="search" aria-label="Filter nodes">
        <label class="filter-label visually-hidden" for="graph-search">Search</label>
        <div class="filter-search-wrap">
          <span class="filter-search-icon" aria-hidden="true">🔍</span>
          <input
            id="graph-search"
            class="filter-search"
            type="search"
            placeholder="${esc(searchPlaceholder)}"
            autocomplete="off"
            aria-controls="graph-results-count"
          />
        </div>
        ${categories.length ? `
        <label class="filter-label visually-hidden" for="graph-category">Filter by category</label>
        <select id="graph-category" class="filter-select" aria-label="Filter by category">
          <option value="">All categories</option>
          ${categories.map(c => `<option value="${esc(c.value)}">${esc(c.label)}</option>`).join('')}
        </select>` : ''}
        <span id="graph-results-count" class="filter-count" aria-live="polite" aria-atomic="true"></span>
      </div>
    `;

    const searchInput = container.querySelector('#graph-search');
    const selectEl   = container.querySelector('#graph-category');
    const countEl    = container.querySelector('#graph-results-count');

    function emit() {
      onChange({ term: _term, category: _category });
    }

    searchInput.addEventListener('input', () => {
      _term = searchInput.value;
      emit();
    });

    if (selectEl) {
      selectEl.addEventListener('change', () => {
        _category = selectEl.value;
        emit();
      });
    }

    function reset() {
      _term = '';
      _category = '';
      searchInput.value = '';
      if (selectEl) selectEl.value = '';
      emit();
    }

    function setCount(n, total) {
      countEl.textContent = n === total ? `${total} nodes` : `${n} / ${total} nodes`;
    }

    function setValue(term, category) {
      _term = term ?? '';
      _category = category ?? '';
      searchInput.value = _term;
      if (selectEl) selectEl.value = _category;
      emit();
    }

    return { reset, setCount, setValue };
  }

  /* ------------------------------------------------------------------ */
  /* Textual Fallback                                                     */
  /* ------------------------------------------------------------------ */

  /**
   * Render entities as an accessible table (fallback for non-interactive view).
   *
   * @param {HTMLElement} container
   * @param {object[]}    entities
   * @param {Array<{key: string, label: string, render?: Function}>} columns
   * @param {object}      [opts]
   * @param {string}      [opts.caption='Entities']
   * @param {Function}    [opts.getRowLink]   — (entity) => string|null
   */
  function renderTextualFallback(container, entities, columns, opts = {}) {
    const { caption = 'Entities', getRowLink = null } = opts;

    if (!entities.length) {
      container.innerHTML = '<p class="text-muted text-sm">No data available.</p>';
      return;
    }

    const headerCells = columns
      .map(c => `<th scope="col">${esc(c.label)}</th>`)
      .join('');

    const rows = entities.map(entity => {
      const cells = columns.map(c => {
        const val = entity[c.key];
        const html = c.render ? c.render(val, entity) : esc(val ?? '—');
        return `<td>${html}</td>`;
      }).join('');

      if (getRowLink) {
        const href = getRowLink(entity);
        if (href) {
          return `<tr tabindex="0" data-href="${esc(href)}" class="table-row-link"
                    onclick="location.href=this.dataset.href"
                    onkeydown="if(event.key==='Enter')location.href=this.dataset.href"
                    role="link" aria-label="View details for ${esc(entity.name || entity.id || '')}">
            ${cells}
          </tr>`;
        }
      }
      return `<tr>${cells}</tr>`;
    }).join('');

    container.innerHTML = `
      <div class="textual-fallback">
        <table class="fallback-table">
          <caption>${esc(caption)}</caption>
          <thead><tr>${headerCells}</tr></thead>
          <tbody>${rows}</tbody>
        </table>
      </div>
    `;
  }

  /* ------------------------------------------------------------------ */
  /* Viewport Warning                                                     */
  /* ------------------------------------------------------------------ */

  /**
   * Insert a banner on small screens advising desktop for full interactivity.
   * Only shown at < 768px; hides automatically on resize.
   *
   * @param {HTMLElement} container — where to insert the warning (top of content)
   * @param {object}      [opts]
   * @param {string}      [opts.message]
   * @param {boolean}     [opts.dismissible=true]
   */
  function renderViewportWarning(container, opts = {}) {
    const {
      message = 'This interactive map is optimised for larger screens. You can still browse the table view below.',
      dismissible = true,
    } = opts;

    const el = document.createElement('div');
    el.className = 'viewport-warning';
    el.setAttribute('role', 'note');
    el.setAttribute('aria-label', 'Screen size notice');
    el.innerHTML = `
      <span class="viewport-warning-icon" aria-hidden="true">📱</span>
      <span class="viewport-warning-text">${esc(message)}</span>
      ${dismissible ? `<button class="viewport-warning-dismiss" aria-label="Dismiss notice">✕</button>` : ''}
    `;

    const dismissBtn = el.querySelector('.viewport-warning-dismiss');
    if (dismissBtn) {
      dismissBtn.addEventListener('click', () => el.remove());
    }

    function update() {
      if (window.innerWidth < 768) {
        if (!container.contains(el)) container.prepend(el);
      } else {
        el.remove();
      }
    }

    update();
    window.addEventListener('resize', update);

    return el;
  }

  /* ------------------------------------------------------------------ */
  /* Freshness Strip                                                      */
  /* ------------------------------------------------------------------ */

  /**
   * Render a data freshness/build status strip.
   *
   * @param {HTMLElement} container
   * @param {object}      manifest   — build-manifest.json contents
   */
  function renderFreshnessStrip(container, manifest) {
    const ts   = manifest?.generated_at ?? 'Unknown';
    const warn = (manifest?.warnings ?? []).length;
    const err  = (manifest?.errors ?? []).length;
    const freshness = manifest?.freshness_status ?? 'UNKNOWN';

    const healthClass = {
      HEALTHY: 'freshness-healthy',
      AT_RISK: 'freshness-at-risk',
      STALE:   'freshness-stale',
      UNKNOWN: 'freshness-unknown',
    }[freshness] ?? 'freshness-unknown';

    const formattedTs = DataLoader?.formatTimestamp
      ? DataLoader.formatTimestamp(ts)
      : ts;

    container.innerHTML = `
      <div class="freshness-strip ${esc(healthClass)}" aria-label="Data freshness">
        <span class="freshness-indicator" aria-hidden="true"></span>
        <span class="freshness-text">
          Data generated: <time datetime="${esc(ts)}">${esc(formattedTs)}</time>
        </span>
        ${warn ? `<span class="freshness-warn" role="note">${warn} warning${warn > 1 ? 's' : ''}</span>` : ''}
        ${err  ? `<span class="freshness-err"  role="alert">${err} error${err > 1 ? 's' : ''}</span>` : ''}
      </div>
    `;
  }

  /* ------------------------------------------------------------------ */
  /* Public API                                                           */
  /* ------------------------------------------------------------------ */

  return {
    renderStatusBadge,
    renderHealthBadge,
    renderLegend,
    renderFilterPanel,
    renderTextualFallback,
    renderViewportWarning,
    renderFreshnessStrip,
  };
})();
