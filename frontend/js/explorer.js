/**
 * NASA FIRE-X Data Explorer Controller
 * Multi-parameter filtering, paginated experiment table, comparison selection, modal inspector
 */

class FireXExplorer {
  constructor() {
    this.currentPage = 1;
    this.limit = 50;
    this.totalPages = 1;
    this.filters = {
      query: '',
      family: '',
      fuel: '',
      outcome: '',
      min_o2: '',
      max_o2: '',
      sort_by: 'experiment_id',
      sort_dir: 'ASC'
    };
    this.comparisonSet = new Set();
    this.maxCompare = 4;
    this.debounceTimer = null;
    this.currentModal = null;
  }

  init() {
    // Search input
    const searchInput = document.getElementById('exp-search-input');
    if (searchInput) {
      searchInput.addEventListener('input', () => {
        this.filters.query = searchInput.value.trim();
        this.debounceLoad(400);
      });
    }

    // Family filter
    const familySelect = document.getElementById('filter-family');
    if (familySelect) {
      familySelect.addEventListener('change', () => {
        this.filters.family = familySelect.value;
        this.currentPage = 1;
        this.load();
      });
    }

    // Fuel filter
    const fuelSelect = document.getElementById('filter-fuel');
    if (fuelSelect) {
      fuelSelect.addEventListener('change', () => {
        this.filters.fuel = fuelSelect.value;
        this.currentPage = 1;
        this.load();
      });
    }

    // Outcome filter
    const outcomeSelect = document.getElementById('filter-outcome');
    if (outcomeSelect) {
      outcomeSelect.addEventListener('change', () => {
        this.filters.outcome = outcomeSelect.value;
        this.currentPage = 1;
        this.load();
      });
    }

    // O2 range sliders
    const o2MinSlider = document.getElementById('filter-o2-min');
    const o2MaxSlider = document.getElementById('filter-o2-max');
    if (o2MinSlider) {
      o2MinSlider.addEventListener('input', () => {
        this.filters.min_o2 = parseFloat(o2MinSlider.value);
        document.getElementById('filter-o2-min-val').textContent = this.filters.min_o2 + '%';
        this.debounceLoad(500);
      });
    }
    if (o2MaxSlider) {
      o2MaxSlider.addEventListener('input', () => {
        this.filters.max_o2 = parseFloat(o2MaxSlider.value);
        document.getElementById('filter-o2-max-val').textContent = this.filters.max_o2 + '%';
        this.debounceLoad(500);
      });
    }

    // Reset filters btn
    const resetBtn = document.getElementById('reset-filters-btn');
    if (resetBtn) {
      resetBtn.addEventListener('click', () => this.resetFilters());
    }

    // Pagination
    const prevBtn = document.getElementById('page-prev-btn');
    const nextBtn = document.getElementById('page-next-btn');
    if (prevBtn) prevBtn.addEventListener('click', () => this.changePage(-1));
    if (nextBtn) nextBtn.addEventListener('click', () => this.changePage(1));

    // Compare panel clear
    const clearCmpBtn = document.getElementById('clear-compare-btn');
    if (clearCmpBtn) clearCmpBtn.addEventListener('click', () => this.clearComparison());

    // Run comparison
    const runCmpBtn = document.getElementById('run-compare-btn');
    if (runCmpBtn) runCmpBtn.addEventListener('click', () => this.runComparison());

    // Modal close
    const modalClose = document.getElementById('inspector-modal-close');
    if (modalClose) modalClose.addEventListener('click', () => this.closeModal());
    const modalOverlay = document.getElementById('inspector-modal-overlay');
    if (modalOverlay) {
      modalOverlay.addEventListener('click', (e) => {
        if (e.target === modalOverlay) this.closeModal();
      });
    }

    // Initial load
    this.load();
  }

  debounceLoad(delay = 350) {
    if (this.debounceTimer) clearTimeout(this.debounceTimer);
    this.debounceTimer = setTimeout(() => {
      this.currentPage = 1;
      this.load();
    }, delay);
  }

  resetFilters() {
    this.filters = { query: '', family: '', fuel: '', outcome: '', min_o2: '', max_o2: '', sort_by: 'experiment_id', sort_dir: 'ASC' };
    this.currentPage = 1;

    const ids = ['exp-search-input', 'filter-family', 'filter-fuel', 'filter-outcome'];
    ids.forEach(id => {
      const el = document.getElementById(id);
      if (el) el.value = '';
    });

    const minSlider = document.getElementById('filter-o2-min');
    const maxSlider = document.getElementById('filter-o2-max');
    if (minSlider) { minSlider.value = 14; document.getElementById('filter-o2-min-val').textContent = '14%'; }
    if (maxSlider) { maxSlider.value = 50; document.getElementById('filter-o2-max-val').textContent = '50%'; }

    this.load();
  }

  changePage(delta) {
    const newPage = this.currentPage + delta;
    if (newPage < 1 || newPage > this.totalPages) return;
    this.currentPage = newPage;
    this.load();
  }

  async load() {
    const params = {
      page: this.currentPage,
      limit: this.limit,
      sort_by: this.filters.sort_by,
      sort_dir: this.filters.sort_dir
    };
    if (this.filters.query) params.query = this.filters.query;
    if (this.filters.family) params.family = this.filters.family;
    if (this.filters.fuel) params.fuel = this.filters.fuel;
    if (this.filters.outcome) params.outcome = this.filters.outcome;
    if (this.filters.min_o2 !== '') params.min_o2 = this.filters.min_o2;
    if (this.filters.max_o2 !== '') params.max_o2 = this.filters.max_o2;

    const tableBody = document.getElementById('experiments-tbody');
    if (tableBody) {
      tableBody.innerHTML = `<tr><td colspan="9" style="text-align:center;padding:40px;color:var(--text-muted)">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="animation:spin 1s linear infinite;display:inline-block;margin-bottom:8px"><path d="M21 12a9 9 0 11-6.219-8.56"/></svg>
        <br>Fetching telemetry data...
      </td></tr>`;
    }

    const result = await window.apiClient.fetchExperiments(params);
    this.totalPages = result.total_pages || 1;

    this.renderTable(result.experiments || [], result.total || 0);
    this.updatePagination(result.total || 0);
  }

  renderTable(rows, total) {
    const lang = window.i18n ? window.i18n.currentLanguage : 'en';
    const tbody = document.getElementById('experiments-tbody');
    if (!tbody) return;

    if (rows.length === 0) {
      const noResultsText = window.i18n ? window.i18n.t('explorer.no_results') : 'No experiments match the specified filter criteria.';
      tbody.innerHTML = `<tr><td colspan="9" style="text-align:center;padding:48px;color:var(--text-muted);font-size:0.9rem">${noResultsText}</td></tr>`;
      return;
    }

    tbody.innerHTML = rows.map(row => {
      const isInCompare = this.comparisonSet.has(row.experiment_id);
      const outcome = row.extinction_outcome || '—';
      const badgeClass = this.getOutcomeBadgeClass(outcome);
      const addText = window.i18n ? window.i18n.t('explorer.action_compare_add') : '+ Compare';
      const removeText = window.i18n ? window.i18n.t('explorer.action_compare_remove') : '— Remove';
      const inspectText = window.i18n ? window.i18n.t('explorer.action_inspect') : 'Inspect';

      return `<tr data-exp-id="${row.experiment_id}">
        <td class="td-id">${row.experiment_id || '—'}</td>
        <td><span class="badge badge-family">${row.dataset_family || '—'}</span></td>
        <td class="td-mono">${row.fuel_material || '—'}</td>
        <td class="td-mono">${row.oxygen_pct != null ? row.oxygen_pct.toFixed(1) : '—'}</td>
        <td class="td-mono">${row.pressure_kpa != null ? row.pressure_kpa.toFixed(1) : '—'}</td>
        <td class="td-mono">${row.burn_time_s != null ? row.burn_time_s.toFixed(1) : '—'}</td>
        <td class="td-mono">${row.extinction_diameter_mm != null ? row.extinction_diameter_mm.toFixed(3) : '—'}</td>
        <td><span class="badge ${badgeClass}">${outcome}</span></td>
        <td style="display:flex;gap:6px;align-items:center">
          <button class="btn btn-outline btn-sm inspect-btn" data-id="${row.experiment_id}" style="font-size:0.72rem">${inspectText}</button>
          <button class="btn btn-sm compare-toggle-btn ${isInCompare ? 'btn-secondary' : 'btn-outline'}" data-id="${row.experiment_id}" style="font-size:0.72rem;min-width:80px">
            ${isInCompare ? removeText : addText}
          </button>
        </td>
      </tr>`;
    }).join('');

    // Attach action listeners
    tbody.querySelectorAll('.inspect-btn').forEach(btn => {
      btn.addEventListener('click', () => this.openModal(btn.getAttribute('data-id')));
    });

    tbody.querySelectorAll('.compare-toggle-btn').forEach(btn => {
      btn.addEventListener('click', () => this.toggleCompare(btn.getAttribute('data-id')));
    });

    // Update results count
    const statsEl = document.getElementById('table-stats-text');
    if (statsEl) {
      const t = window.i18n ? window.i18n.t('explorer.showing_results', { count: rows.length, total }) : `Showing ${rows.length} of ${total} experiments`;
      statsEl.textContent = t;
    }
  }

  getOutcomeBadgeClass(outcome) {
    const o = (outcome || '').toLowerCase();
    if (o.includes('extinguish') || o.includes('quench')) return 'badge-quenched';
    if (o.includes('radiativ')) return 'badge-radiative';
    if (o.includes('sustain') || o.includes('burn') || o.includes('continue')) return 'badge-sustained';
    return 'badge-family';
  }

  updatePagination(total) {
    const prevBtn = document.getElementById('page-prev-btn');
    const nextBtn = document.getElementById('page-next-btn');
    const pageInfo = document.getElementById('page-info-text');

    if (prevBtn) prevBtn.disabled = this.currentPage <= 1;
    if (nextBtn) nextBtn.disabled = this.currentPage >= this.totalPages;
    if (pageInfo) {
      const t = window.i18n ? window.i18n.t('explorer.page_info', { page: this.currentPage, pages: this.totalPages }) : `Page ${this.currentPage} of ${this.totalPages}`;
      pageInfo.textContent = t;
    }
  }

  // Comparison
  toggleCompare(expId) {
    if (this.comparisonSet.has(expId)) {
      this.comparisonSet.delete(expId);
    } else {
      if (this.comparisonSet.size >= this.maxCompare) {
        alert(window.i18n
          ? (window.i18n.currentLanguage === 'az' ? 'Maksimum 4 eksperiment seçə bilərsiniz.' : 'Maximum 4 experiments can be selected for comparison.')
          : 'Maximum 4 experiments can be selected.');
        return;
      }
      this.comparisonSet.add(expId);
    }
    this.updateComparePanel();
    this.load(); // Re-render table to update button states
  }

  updateComparePanel() {
    const panel = document.getElementById('compare-panel');
    const countEl = document.getElementById('compare-count-text');
    const runBtn = document.getElementById('run-compare-btn');

    if (countEl) {
      const t = window.i18n
        ? window.i18n.t('comparison.compare_count', { count: this.comparisonSet.size })
        : `${this.comparisonSet.size} of 4 experiments selected`;
      countEl.textContent = t;
    }

    if (panel) {
      panel.style.display = this.comparisonSet.size > 0 ? 'flex' : 'none';
    }

    if (runBtn) runBtn.disabled = this.comparisonSet.size < 2;
  }

  clearComparison() {
    this.comparisonSet.clear();
    this.updateComparePanel();
    document.getElementById('comparison-results-area').innerHTML = '';
    this.load();
  }

  async runComparison() {
    const ids = [...this.comparisonSet];
    const data = await window.apiClient.compareExperiments(ids);
    if (!data) return;

    this.renderComparisonResults(data);
  }

  renderComparisonResults(data) {
    const area = document.getElementById('comparison-results-area');
    if (!area) return;

    const exps = data.experiments;
    if (!exps || exps.length === 0) {
      area.innerHTML = '<p style="color:var(--text-muted)">No comparison data available.</p>';
      return;
    }

    const metrics = [
      { key: 'oxygen_pct', label: 'O₂ (%)', unit: '%', fixed: 1 },
      { key: 'pressure_kpa', label: 'Pressure (kPa)', unit: 'kPa', fixed: 1 },
      { key: 'burn_time_s', label: 'Burn Time (s)', unit: 's', fixed: 1 },
      { key: 'extinction_diameter_mm', label: 'Extinction dₑ (mm)', unit: 'mm', fixed: 3 },
      { key: 'airflow_velocity_cms', label: 'Airflow (cm/s)', unit: 'cm/s', fixed: 2 },
      { key: 'flame_temp_k', label: 'Flame Temp (K)', unit: 'K', fixed: 0 }
    ];

    area.innerHTML = `
      <div class="table-responsive" style="margin-top:20px">
        <table class="data-table">
          <thead>
            <tr>
              <th>Metric</th>
              ${exps.map(e => `<th class="td-id">${e.experiment_id}</th>`).join('')}
            </tr>
            <tr style="background:rgba(0,229,255,0.04)">
              <th style="color:var(--text-muted);font-weight:400;font-size:0.72rem">Family / Fuel</th>
              ${exps.map(e => `<th style="color:var(--text-secondary);font-weight:500">${e.dataset_family} / ${e.fuel_material || '—'}</th>`).join('')}
            </tr>
          </thead>
          <tbody>
            ${metrics.map(m => {
              const vals = exps.map(e => e[m.key]);
              const numVals = vals.filter(v => v != null);
              const maxVal = numVals.length ? Math.max(...numVals) : null;
              const minVal = numVals.length ? Math.min(...numVals) : null;

              return `<tr>
                <td style="font-size:0.78rem;color:var(--text-muted);font-weight:600;text-transform:uppercase;letter-spacing:0.04em">${m.label}</td>
                ${exps.map(e => {
                  const v = e[m.key];
                  if (v == null) return `<td class="td-mono">—</td>`;
                  const formatted = typeof v === 'number' ? v.toFixed(m.fixed) : v;
                  const isMax = v === maxVal && numVals.length > 1;
                  const isMin = v === minVal && numVals.length > 1;
                  const color = isMax ? 'color:var(--color-amber)' : isMin ? 'color:var(--color-emerald)' : '';
                  return `<td class="td-mono" style="${color}">${formatted} ${m.unit}</td>`;
                }).join('')}
              </tr>`;
            }).join('')}
            <tr>
              <td style="font-size:0.78rem;color:var(--text-muted);font-weight:600;text-transform:uppercase">Outcome</td>
              ${exps.map(e => {
                const o = e.extinction_outcome || '—';
                return `<td><span class="badge ${this.getOutcomeBadgeClass(o)}">${o}</span></td>`;
              }).join('')}
            </tr>
          </tbody>
        </table>
      </div>
      <p style="font-size:0.72rem;color:var(--text-muted);margin-top:8px;font-family:var(--font-mono)">
        Amber = Maximum value &nbsp;|&nbsp; Green = Minimum value
      </p>
    `;
  }

  // Modal Inspector
  async openModal(expId) {
    const data = await window.apiClient.fetchExperimentById(expId);
    if (!data) return;

    this.currentModal = data;
    this.renderModal(data);

    const overlay = document.getElementById('inspector-modal-overlay');
    if (overlay) {
      overlay.classList.add('open');
      document.body.style.overflow = 'hidden';
    }

    // Set AI context to this experiment
    if (window.aiAssistant) {
      window.aiAssistant.setPageContext({
        section: 'Experiment Inspector',
        experiment_id: data.experiment_id,
        family: data.dataset_family,
        fuel: data.fuel_material,
        oxygen_pct: data.oxygen_pct ? data.oxygen_pct + '%' : 'N/A',
        burn_time_s: data.burn_time_s ? data.burn_time_s + ' s' : 'N/A',
        extinction_outcome: data.extinction_outcome || 'N/A'
      });
    }
  }

  renderModal(data) {
    const fields = [
      ['Canonical ID', data.experiment_id],
      ['Original NASA Test ID', data.original_test_id],
      ['Investigation', data.investigation_id],
      ['Dataset Family', data.dataset_family],
      ['Fuel / Material', data.fuel_material],
      ['Sample Description', data.sample_description],
      ['Material Category', data.material_category],
      ['O₂ Concentration', data.oxygen_pct != null ? data.oxygen_pct.toFixed(1) + ' %' : '—'],
      ['Pressure', data.pressure_kpa != null ? data.pressure_kpa.toFixed(1) + ' kPa' : '—'],
      ['Burn Time', data.burn_time_s != null ? data.burn_time_s.toFixed(1) + ' s' : '—'],
      ['Extinction dₑ', data.extinction_diameter_mm != null ? data.extinction_diameter_mm.toFixed(3) + ' mm' : '—'],
      ['Initial Diameter', data.initial_diameter_mm != null ? data.initial_diameter_mm.toFixed(2) + ' mm' : '—'],
      ['Burning Rate', data.burning_rate_mms != null ? data.burning_rate_mms.toFixed(3) + ' mm/s' : '—'],
      ['Airflow Velocity', data.airflow_velocity_cms != null ? data.airflow_velocity_cms.toFixed(2) + ' cm/s' : '—'],
      ['Flame Temperature', data.flame_temp_k != null ? data.flame_temp_k.toFixed(0) + ' K' : '—'],
      ['Ignition Power', data.ignition_power_w != null ? data.ignition_power_w.toFixed(1) + ' W' : '—'],
      ['Gravity Regime', data.gravity_condition || '—'],
      ['Extinction Outcome', data.extinction_outcome || '—'],
      ['Data Source', data.source_name || '—']
    ];

    const modalTitle = document.getElementById('inspector-modal-title');
    if (modalTitle) modalTitle.textContent = `Telemetry: ${data.experiment_id}`;

    const grid = document.getElementById('inspector-fields-grid');
    if (grid) {
      grid.innerHTML = fields.map(([label, value]) => `
        <div class="inspector-item">
          <div class="inspector-label">${label}</div>
          <div class="inspector-value">${value || '—'}</div>
        </div>
      `).join('');
    }

    if (data.notes) {
      const notesEl = document.getElementById('inspector-notes');
      if (notesEl) {
        notesEl.style.display = 'block';
        notesEl.querySelector('.notes-body').textContent = data.notes;
      }
    }

    // AI button in modal
    const aiBtn = document.getElementById('modal-ask-ai-btn');
    if (aiBtn) {
      aiBtn.onclick = () => {
        this.closeModal();
        const lang = window.i18n ? window.i18n.currentLanguage : 'en';
        const prompt = lang === 'az'
          ? `Bu eksperimenti ətraflı izah et: ${data.experiment_id}, yanacaq: ${data.fuel_material}, O2: ${data.oxygen_pct}%`
          : `Explain this NASA experiment in detail: ${data.experiment_id}, Fuel: ${data.fuel_material}, O₂: ${data.oxygen_pct}%`;
        window.aiAssistant.openPanel();
        window.aiAssistant.inputField.value = prompt;
      };
    }
  }

  closeModal() {
    const overlay = document.getElementById('inspector-modal-overlay');
    if (overlay) {
      overlay.classList.remove('open');
      document.body.style.overflow = '';
    }
    this.currentModal = null;
  }
}

window.explorer = new FireXExplorer();
