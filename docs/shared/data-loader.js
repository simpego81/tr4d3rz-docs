/**
 * TR4D3RZ Project Map — Data Loader
 *
 * Centralized module for loading JSON datasets from docs/data/generated/
 * with error handling, caching, and graceful degradation.
 */

const DataLoader = (() => {
  const CACHE = new Map();
  // Pages at depth 1 (docs/) set window.DATA_BASE_URL = 'data/generated/';
  // Pages at depth 2+ (docs/maps/, docs/details/…) keep the default.
  const BASE_URL = (typeof window !== 'undefined' && window.DATA_BASE_URL !== undefined)
    ? window.DATA_BASE_URL
    : '../data/generated/';

  /**
   * Load JSON dataset with error handling
   *
   * @param {string} filename - Dataset filename (e.g., 'roadmap.json')
   * @param {Object} options - Options {cache: true, fallback: null}
   * @returns {Promise<Object>} Parsed JSON data
   * @throws {DataLoadError} If fetch fails and no fallback available
   */
  async function loadDataset(filename, options = {}) {
    const { cache = true, fallback = null } = options;

    // Check cache
    if (cache && CACHE.has(filename)) {
      return CACHE.get(filename);
    }

    try {
      const url = `${BASE_URL}${filename}`;
      const response = await fetch(url);

      if (!response.ok) {
        throw new DataLoadError(
          `MAP-E005`,
          `Failed to load ${filename}: HTTP ${response.status}`,
          { filename, status: response.status }
        );
      }

      const data = await response.json();

      // Validate schema_version if present
      if (data.schema_version && !isCompatibleVersion(data.schema_version)) {
        console.warn(`[DataLoader] Schema version mismatch: ${data.schema_version} (expected 1.x.x)`);
      }

      // Cache result
      if (cache) {
        CACHE.set(filename, data);
      }

      return data;

    } catch (error) {
      if (fallback) {
        console.warn(`[DataLoader] Using fallback for ${filename}:`, error.message);
        return fallback;
      }

      throw error;
    }
  }

  /**
   * Load build manifest (metadata about generation)
   *
   * @returns {Promise<Object>} Build manifest
   */
  async function loadManifest() {
    return loadDataset('build-manifest.json', {
      fallback: {
        schema_version: '1.0.0',
        generated_at: 'unknown',
        freshness_status: 'UNKNOWN',
        errors: [],
        warnings: []
      }
    });
  }

  /**
   * Load roadmap dataset (milestones + tasks)
   *
   * @returns {Promise<Object>} Roadmap data {milestones, tasks}
   */
  async function loadRoadmap() {
    return loadDataset('roadmap.json', {
      fallback: {
        schema_version: '1.0.0',
        milestones: [],
        tasks: []
      }
    });
  }

  /**
   * Check if schema version is compatible (major version match)
   *
   * @param {string} version - Semantic version string (e.g., "1.2.3")
   * @returns {boolean} True if compatible
   */
  function isCompatibleVersion(version) {
    const [major] = version.split('.');
    return major === '1'; // Accept any 1.x.x version
  }

  /**
   * Custom error for data loading failures
   */
  class DataLoadError extends Error {
    constructor(code, message, context = {}) {
      super(message);
      this.name = 'DataLoadError';
      this.code = code;
      this.context = context;
    }
  }

  /**
   * Render error state in DOM element
   *
   * @param {HTMLElement} container - Container to render error in
   * @param {Error} error - Error object
   */
  function renderError(container, error) {
    const code = error.code || 'MAP-E005';
    const message = error.message || 'Unknown error';

    container.innerHTML = `
      <div class="error" role="alert">
        <div class="error-title">⚠️ Data Load Error [${code}]</div>
        <p>${escapeHtml(message)}</p>
        <p class="text-sm">
          The dataset could not be loaded. This may be due to:
        </p>
        <ul class="text-sm" style="margin-left: 1.5rem; margin-top: 0.5rem;">
          <li>Build pipeline not run (try: <code>python scripts/build_project_map.py</code>)</li>
          <li>Dataset file missing or corrupted</li>
          <li>Network error (check browser console)</li>
        </ul>
      </div>
    `;
  }

  /**
   * Render loading state in DOM element
   *
   * @param {HTMLElement} container - Container to render loading state in
   */
  function renderLoading(container) {
    container.innerHTML = `
      <div class="loading" role="status">
        <span>Loading data...</span>
      </div>
    `;
  }

  /**
   * Escape HTML to prevent XSS
   *
   * @param {string} unsafe - Unsafe string
   * @returns {string} Escaped string
   */
  function escapeHtml(unsafe) {
    return unsafe
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  /**
   * Format ISO timestamp to human-readable string
   *
   * @param {string} isoString - ISO 8601 timestamp
   * @returns {string} Formatted date
   */
  function formatTimestamp(isoString) {
    try {
      const date = new Date(isoString);
      return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    } catch {
      return isoString;
    }
  }

  /**
   * Get badge CSS class for status
   *
   * @param {string} status - Status enum value
   * @returns {string} CSS class name
   */
  function getStatusBadgeClass(status) {
    const normalized = (status || 'unknown').toLowerCase().replace(/_/g, '-');
    return `badge badge-status-${normalized}`;
  }

  /**
   * Get badge CSS class for health
   *
   * @param {string} health - Health enum value
   * @returns {string} CSS class name
   */
  function getHealthBadgeClass(health) {
    const normalized = (health || 'unknown').toLowerCase().replace(/_/g, '-');
    return `badge badge-health-${normalized}`;
  }

  // Public API
  return {
    loadDataset,
    loadManifest,
    loadRoadmap,
    renderError,
    renderLoading,
    escapeHtml,
    formatTimestamp,
    getStatusBadgeClass,
    getHealthBadgeClass,
    DataLoadError
  };
})();
