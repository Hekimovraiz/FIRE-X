/**
 * NASA FIRE-X Platform — Main Application Orchestrator
 * Bootstraps all modules, initializes data, wires up navigation, clock and theme.
 */

class FireXApp {
  constructor() {
    this.initialized = false;
    this.statsData = null;
    this.activeSection = 'dashboard';
  }

  async init() {
    if (this.initialized) return;

    // 1. Init i18n engine
    await window.i18n.init();

    // 2. Start UTC mission clock
    this.startMissionClock();

    // 3. Navigation & section routing
    this.initNavigation();

    // 4. Language switcher
    const langBtn = document.getElementById('lang-toggle-btn');
    if (langBtn) {
      langBtn.addEventListener('click', () => {
        const newLang = window.i18n.toggleLanguage();
        // Reload charts with translated labels if needed
        if (this.statsData) {
          window.chartsEngine.init(this.statsData);
        }
        // Reload simulator in new language
        window.simulator.renderScenario && window.simulator.loadScenario(window.simulator.currentScenario);
      });
    }

    // 5. Mobile nav toggle
    const mobileToggle = document.getElementById('mobile-nav-toggle');
    const navMenu = document.getElementById('main-nav-menu');
    if (mobileToggle && navMenu) {
      mobileToggle.addEventListener('click', () => navMenu.classList.toggle('open'));
    }

    // 6. Fetch stats and initialize charts
    this.statsData = await window.apiClient.fetchStats();
    if (this.statsData) {
      this.populateKPICards(this.statsData);
      window.chartsEngine.init(this.statsData);
    }

    // 7. Populate filter dropdowns from stats families/fuels
    if (this.statsData) {
      this.populateFilterDropdowns(this.statsData);
    }

    // 8. Initialize explorer module
    window.explorer.init();

    // 9. Initialize simulator module
    window.simulator.init();

    // 10. Initialize AI assistant
    window.aiAssistant.init();

    // 11. Set initial AI context
    window.aiAssistant.setPageContext({ section: 'Mission Control Dashboard' });

    // 12. Add keyboard shortcut: "/" focuses search
    document.addEventListener('keydown', (e) => {
      if (e.key === '/' && document.activeElement.tagName !== 'INPUT' && document.activeElement.tagName !== 'TEXTAREA') {
        e.preventDefault();
        const searchInput = document.getElementById('exp-search-input');
        if (searchInput) {
          this.navigateTo('explorer');
          searchInput.focus();
        }
      }
    });

    this.initialized = true;
    console.log('[FIRE-X] Platform initialized successfully.');
  }

  startMissionClock() {
    const updateClock = () => {
      const now = new Date();
      const utc = now.toUTCString().replace('GMT', 'UTC');
      const timeOnly = now.toISOString().replace('T', ' ').substring(0, 19) + ' UTC';
      const clockEl = document.getElementById('mission-clock-val');
      if (clockEl) clockEl.textContent = timeOnly;
    };
    updateClock();
    setInterval(updateClock, 1000);
  }

  initNavigation() {
    const navLinks = document.querySelectorAll('[data-section]');
    navLinks.forEach(link => {
      link.addEventListener('click', (e) => {
        e.preventDefault();
        const section = link.getAttribute('data-section');
        this.navigateTo(section);
      });
    });

    // Smooth scroll for CTA hero buttons
    document.querySelectorAll('[data-scroll-to]').forEach(btn => {
      btn.addEventListener('click', () => {
        const target = document.getElementById(btn.getAttribute('data-scroll-to'));
        if (target) {
          target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      });
    });
  }

  navigateTo(sectionId) {
    // Update active nav link
    document.querySelectorAll('[data-section]').forEach(link => {
      link.classList.toggle('active', link.getAttribute('data-section') === sectionId);
    });

    // Scroll section into view
    const sectionEl = document.getElementById(`section-${sectionId}`);
    if (sectionEl) {
      sectionEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    this.activeSection = sectionId;

    // Update AI context for the section
    if (window.aiAssistant) {
      const contextMap = {
        'dashboard': { section: 'Mission Control Dashboard' },
        'visualizations': { section: 'Analytics Hub — Combustion Telemetry Charts' },
        'explorer': { section: 'Data Explorer — 484 NASA Experiments' },
        'simulator': { section: 'Planetary Mission Fire Hazard Simulator' },
        'compare': { section: 'Multi-Experiment Comparison Tool' }
      };
      window.aiAssistant.setPageContext(contextMap[sectionId] || { section: sectionId });
    }
  }

  populateKPICards(stats) {
    const setKPI = (id, val) => {
      const el = document.getElementById(id);
      if (el) el.textContent = val;
    };

    setKPI('kpi-total-experiments', stats.total_experiments?.toLocaleString() || '484');
    setKPI('kpi-total-families', stats.total_families || '16');
    setKPI('kpi-avg-o2', stats.averages ? stats.averages.avg_oxygen_pct.toFixed(1) + '%' : '—');
    setKPI('kpi-avg-de', stats.averages ? stats.averages.avg_extinction_diameter_mm.toFixed(2) + ' mm' : '—');
  }

  populateFilterDropdowns(stats) {
    // Families
    const familySelect = document.getElementById('filter-family');
    if (familySelect && stats.families_distribution) {
      const opts = stats.families_distribution.map(f =>
        `<option value="${f.family}">${f.family} (${f.count})</option>`
      ).join('');
      familySelect.innerHTML = `<option value="">${window.i18n.t('explorer.filter_all')}</option>` + opts;
    }

    // Fuels
    const fuelSelect = document.getElementById('filter-fuel');
    if (fuelSelect && stats.top_fuels) {
      const opts = stats.top_fuels.map(f =>
        `<option value="${f.fuel}">${f.fuel} (${f.count})</option>`
      ).join('');
      fuelSelect.innerHTML = `<option value="">${window.i18n.t('explorer.filter_all')}</option>` + opts;
    }

    // Outcomes
    const outcomeSelect = document.getElementById('filter-outcome');
    if (outcomeSelect && stats.outcomes) {
      const opts = stats.outcomes.map(o =>
        `<option value="${o.outcome}">${o.outcome} (${o.count})</option>`
      ).join('');
      outcomeSelect.innerHTML = `<option value="">${window.i18n.t('explorer.filter_all')}</option>` + opts;
    }
  }
}

// Bootstrap app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  window.app = new FireXApp();
  window.app.init().catch(err => console.error('[FIRE-X] Initialization error:', err));
});

// Add spin animation for loading state
const spinStyle = document.createElement('style');
spinStyle.textContent = `@keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }`;
document.head.appendChild(spinStyle);
