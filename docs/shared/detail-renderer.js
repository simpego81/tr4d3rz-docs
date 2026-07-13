/**
 * TR4D3RZ Project Map — Detail Page Renderer
 *
 * Renders a single entity (milestone or task) into a detail page container.
 * All required fields are shown explicitly; missing optional fields show "—".
 *
 * Usage:
 *   DetailRenderer.render(container, entity, opts)
 *
 * entity shape: roadmap.json milestones[]/tasks[] element with raw_data.
 */

const DetailRenderer = (() => {
  'use strict';

  /* ------------------------------------------------------------------ */
  /* Entry point                                                          */
  /* ------------------------------------------------------------------ */

  /**
   * Render entity into container.
   *
   * @param {HTMLElement} container
   * @param {object}      entity     — roadmap entity with raw_data
   * @param {object}      [opts]
   * @param {object}      [opts.allEntities]  — {id: entity} map for cross-links
   */
  function render(container, entity, opts = {}) {
    const d = entity.raw_data || entity;
    const allEntities = opts.allEntities || {};

    container.innerHTML = '';
    container.appendChild(_buildBreadcrumb(entity));
    container.appendChild(_buildHeader(d));
    container.appendChild(_buildMetaStrip(d));
    container.appendChild(_buildSummary(d));

    const body = document.createElement('div');
    body.className = 'detail-body';

    body.appendChild(_buildSection('Owners',       _renderOwners(d.owners)));
    body.appendChild(_buildSection('Dependencies', _renderDependencies(d.dependencies, allEntities)));
    body.appendChild(_buildSection('Blockers',     _renderBlockers(d.blockers)));

    if (d.tasks?.length)               body.appendChild(_buildSection('Tasks',                _renderSubTasks(d.tasks, allEntities)));
    if (d.outcome)                     body.appendChild(_buildSection('Outcome',              _renderText(d.outcome)));
    if (d.acceptance_criteria?.length) body.appendChild(_buildSection('Acceptance Criteria',  _renderChecklist(d.acceptance_criteria)));
    if (d.outputs?.length)             body.appendChild(_buildSection('Outputs',              _renderList(d.outputs)));

    body.appendChild(_buildSection('Evidence',    _renderEvidence(d.evidence)));
    body.appendChild(_buildSection('Source Refs', _renderSourceRefs(d.source_refs)));

    container.appendChild(body);
    container.appendChild(_buildBackLink());
  }

  /* ------------------------------------------------------------------ */
  /* Breadcrumb                                                           */
  /* ------------------------------------------------------------------ */

  function _buildBreadcrumb(entity) {
    const nav = document.createElement('nav');
    nav.setAttribute('aria-label', 'Breadcrumb');
    nav.className = 'breadcrumb';

    const mapHref = '../../index-new.html';
    const roadmapHref = '../../maps/roadmap.html';
    const kind = entity.kind || 'entity';

    nav.innerHTML = `
      <a href="${mapHref}">Project Map</a>
      <span class="breadcrumb-separator" aria-hidden="true">/</span>
      <a href="${roadmapHref}">Roadmap</a>
      <span class="breadcrumb-separator" aria-hidden="true">/</span>
      <span aria-current="page">${esc(entity.name || entity.id)}</span>
    `;
    return nav;
  }

  /* ------------------------------------------------------------------ */
  /* Header                                                               */
  /* ------------------------------------------------------------------ */

  function _buildHeader(d) {
    const header = document.createElement('div');
    header.className = 'detail-header';

    const kindLabel = (d.kind || d.id?.startsWith('m') ? 'Milestone' : 'Task');

    header.innerHTML = `
      <div class="detail-header-badges">
        <span class="badge badge-kind">${esc(d.kind || kindLabel)}</span>
        ${Components.renderStatusBadge(d.status)}
        ${Components.renderHealthBadge(d.health)}
      </div>
      <h1 class="detail-title">${esc(d.name || d.id)}</h1>
    `;
    return header;
  }

  /* ------------------------------------------------------------------ */
  /* Meta strip (dates, freshness, critical path)                        */
  /* ------------------------------------------------------------------ */

  function _buildMetaStrip(d) {
    const strip = document.createElement('div');
    strip.className = 'detail-meta-strip';

    const updatedAt  = d.updated_at  ? DataLoader.formatTimestamp(d.updated_at)  : '—';
    const startDate  = d.start_date  || '—';
    const endDate    = d.end_date    || '—';
    const freshness  = d.freshness   || 'UNKNOWN';
    const critical   = d.critical_path ? 'Yes' : 'No';

    strip.innerHTML = `
      <dl class="meta-grid">
        <div class="meta-item">
          <dt class="meta-label">Updated</dt>
          <dd class="meta-value">
            <time datetime="${esc(d.updated_at || '')}">${esc(updatedAt)}</time>
          </dd>
        </div>
        <div class="meta-item">
          <dt class="meta-label">Freshness</dt>
          <dd class="meta-value">
            <span class="freshness-tag freshness-tag-${esc(freshness.toLowerCase())}">${esc(freshness)}</span>
          </dd>
        </div>
        <div class="meta-item">
          <dt class="meta-label">Start date</dt>
          <dd class="meta-value">${esc(startDate)}</dd>
        </div>
        <div class="meta-item">
          <dt class="meta-label">End date</dt>
          <dd class="meta-value">${esc(endDate)}</dd>
        </div>
        <div class="meta-item">
          <dt class="meta-label">Critical path</dt>
          <dd class="meta-value">${esc(critical)}</dd>
        </div>
        ${d.estimated_effort ? `
        <div class="meta-item">
          <dt class="meta-label">Effort</dt>
          <dd class="meta-value">${esc(d.estimated_effort)}</dd>
        </div>` : ''}
      </dl>
    `;
    return strip;
  }

  /* ------------------------------------------------------------------ */
  /* Summary                                                              */
  /* ------------------------------------------------------------------ */

  function _buildSummary(d) {
    const el = document.createElement('div');
    el.className = 'detail-summary';
    el.innerHTML = `<p>${esc(d.summary || '—')}</p>`;
    return el;
  }

  /* ------------------------------------------------------------------ */
  /* Section wrapper                                                      */
  /* ------------------------------------------------------------------ */

  function _buildSection(title, contentEl) {
    const section = document.createElement('section');
    section.className = 'detail-section';
    section.setAttribute('aria-labelledby', `section-${title.toLowerCase().replace(/\s+/g, '-')}`);

    const h2 = document.createElement('h2');
    h2.className = 'detail-section-title';
    h2.id = `section-${title.toLowerCase().replace(/\s+/g, '-')}`;
    h2.textContent = title;

    section.appendChild(h2);
    if (contentEl) section.appendChild(contentEl);
    return section;
  }

  /* ------------------------------------------------------------------ */
  /* Owners                                                               */
  /* ------------------------------------------------------------------ */

  function _renderOwners(owners) {
    const el = document.createElement('div');
    if (!owners?.length) {
      el.innerHTML = '<p class="detail-empty">— No owners defined</p>';
      return el;
    }
    el.innerHTML = `
      <ul class="detail-list">
        ${owners.map(o => `
          <li class="detail-list-item">
            <span class="owner-agent">${esc(o.agent || '—')}</span>
            <span class="owner-role text-muted">${esc(o.role || '')}</span>
          </li>`).join('')}
      </ul>`;
    return el;
  }

  /* ------------------------------------------------------------------ */
  /* Dependencies                                                         */
  /* ------------------------------------------------------------------ */

  function _renderDependencies(deps, allEntities) {
    const el = document.createElement('div');
    if (!deps?.length) {
      el.innerHTML = '<p class="detail-empty">— None</p>';
      return el;
    }
    const items = deps.map(id => {
      const linked = allEntities[id];
      if (linked) {
        const url = linked.raw_data?.detail_url
          ? `../../${linked.raw_data.detail_url}`
          : '#';
        return `<li class="detail-list-item">
          <a href="${url}">${esc(linked.name || id)}</a>
          ${Components.renderStatusBadge(linked.raw_data?.status)}
        </li>`;
      }
      return `<li class="detail-list-item"><span class="text-muted">${esc(id)}</span></li>`;
    }).join('');
    el.innerHTML = `<ul class="detail-list">${items}</ul>`;
    return el;
  }

  /* ------------------------------------------------------------------ */
  /* Blockers                                                             */
  /* ------------------------------------------------------------------ */

  function _renderBlockers(blockers) {
    const el = document.createElement('div');
    if (!blockers?.length) {
      el.innerHTML = '<p class="detail-empty">— None</p>';
      return el;
    }
    const items = blockers.map(b => `
      <li class="detail-list-item blocker-item">
        <span class="blocker-severity blocker-${esc((b.severity||'').toLowerCase())}">${esc(b.severity || 'UNKNOWN')}</span>
        <span class="blocker-desc">${esc(b.description || '—')}</span>
        ${b.ref ? `<a class="blocker-ref text-xs" href="#" title="${esc(b.ref)}">ref</a>` : ''}
      </li>`).join('');
    el.innerHTML = `<ul class="detail-list">${items}</ul>`;
    return el;
  }

  /* ------------------------------------------------------------------ */
  /* Sub-tasks (for milestones)                                           */
  /* ------------------------------------------------------------------ */

  function _renderSubTasks(taskIds, allEntities) {
    const el = document.createElement('div');
    const items = taskIds.map(id => {
      const linked = allEntities[id];
      if (linked) {
        const url = linked.raw_data?.detail_url
          ? `../../${linked.raw_data.detail_url}`
          : '#';
        const status = linked.raw_data?.status || 'UNKNOWN';
        return `<li class="detail-list-item">
          <a href="${url}">${esc(linked.name || id)}</a>
          ${Components.renderStatusBadge(status)}
          ${Components.renderHealthBadge(linked.raw_data?.health)}
        </li>`;
      }
      return `<li class="detail-list-item text-muted">${esc(id)}</li>`;
    }).join('');
    el.innerHTML = `<ul class="detail-list">${items || '<li class="detail-empty">— None</li>'}</ul>`;
    return el;
  }

  /* ------------------------------------------------------------------ */
  /* Acceptance criteria checklist                                        */
  /* ------------------------------------------------------------------ */

  function _renderChecklist(criteria) {
    const el = document.createElement('div');
    if (!criteria?.length) {
      el.innerHTML = '<p class="detail-empty">— None defined</p>';
      return el;
    }
    const items = criteria.map(c => `
      <li class="detail-list-item checklist-item">
        <span class="checklist-icon" aria-hidden="true">◻</span>
        ${esc(c)}
      </li>`).join('');
    el.innerHTML = `<ul class="detail-list" role="list">${items}</ul>`;
    return el;
  }

  /* ------------------------------------------------------------------ */
  /* Outputs list                                                         */
  /* ------------------------------------------------------------------ */

  function _renderList(items) {
    const el = document.createElement('div');
    if (!items?.length) {
      el.innerHTML = '<p class="detail-empty">— None</p>';
      return el;
    }
    el.innerHTML = `
      <ul class="detail-list">
        ${items.map(i => `<li class="detail-list-item">${esc(i)}</li>`).join('')}
      </ul>`;
    return el;
  }

  /* ------------------------------------------------------------------ */
  /* Plain text block                                                     */
  /* ------------------------------------------------------------------ */

  function _renderText(text) {
    const el = document.createElement('div');
    el.innerHTML = `<p>${esc(text || '—')}</p>`;
    return el;
  }

  /* ------------------------------------------------------------------ */
  /* Evidence                                                             */
  /* ------------------------------------------------------------------ */

  function _renderEvidence(evidence) {
    const el = document.createElement('div');
    if (!evidence?.length) {
      el.innerHTML = '<p class="detail-empty">— No evidence recorded</p>';
      return el;
    }
    const items = evidence.map(e => {
      const date = e.date ? DataLoader.formatTimestamp(e.date) : '—';
      const link = e.url
        ? `<a href="${esc(e.url)}" target="_blank" rel="noopener">${esc(e.title || e.url)}</a>`
        : esc(e.title || '—');
      return `<li class="detail-list-item evidence-item">
        <span class="evidence-type badge">${esc(e.type || '?')}</span>
        <span class="evidence-title">${link}</span>
        <time class="evidence-date text-xs text-muted" datetime="${esc(e.date || '')}">${esc(date)}</time>
      </li>`;
    }).join('');
    el.innerHTML = `<ul class="detail-list">${items}</ul>`;
    return el;
  }

  /* ------------------------------------------------------------------ */
  /* Source refs                                                          */
  /* ------------------------------------------------------------------ */

  function _renderSourceRefs(refs) {
    const el = document.createElement('div');
    if (!refs?.length) {
      el.innerHTML = '<p class="detail-empty">— No source references</p>';
      return el;
    }
    const items = refs.map(r => {
      const hash = r.hash ? r.hash.substring(0, 8) + '…' : '—';
      const extracted = r.extracted_at ? DataLoader.formatTimestamp(r.extracted_at) : '—';
      return `<li class="detail-list-item source-ref-item">
        <code class="source-path">${esc(r.path || '—')}</code>
        <span class="source-hash text-xs text-muted" title="${esc(r.hash || '')}">sha256:${esc(hash)}</span>
        <span class="source-date text-xs text-muted">${esc(extracted)}</span>
      </li>`;
    }).join('');
    el.innerHTML = `<ul class="detail-list source-refs">${items}</ul>`;
    return el;
  }

  /* ------------------------------------------------------------------ */
  /* Back link                                                            */
  /* ------------------------------------------------------------------ */

  function _buildBackLink() {
    const el = document.createElement('div');
    el.className = 'detail-back';
    el.innerHTML = `<a href="../../maps/roadmap.html" class="back-link">← Back to Roadmap</a>`;
    return el;
  }

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
  /* Public API                                                           */
  /* ------------------------------------------------------------------ */

  return { render };
})();
