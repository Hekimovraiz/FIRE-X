/**
 * NASA FIRE-X Planetary Scenario Simulator Controller
 * Renders hazard meters, metric panels, and advisory cards
 */

class FireXSimulator {
  constructor() {
    this.currentScenario = 'iss';
    this.customO2 = 21.0;
    this.customPressure = 101.3;
    this.debounceTimer = null;
  }

  init() {
    // Preset card click handlers
    document.querySelectorAll('.preset-card').forEach(card => {
      card.addEventListener('click', () => {
        const sid = card.getAttribute('data-scenario');
        this.selectPreset(sid);
      });
    });

    // Custom sliders
    const o2Slider = document.getElementById('slider-custom-o2');
    const pressureSlider = document.getElementById('slider-custom-pressure');

    if (o2Slider) {
      o2Slider.addEventListener('input', () => {
        this.customO2 = parseFloat(o2Slider.value);
        document.getElementById('val-custom-o2').textContent = this.customO2.toFixed(1) + '%';
        this.debouncedFetch();
      });
    }

    if (pressureSlider) {
      pressureSlider.addEventListener('input', () => {
        this.customPressure = parseFloat(pressureSlider.value);
        document.getElementById('val-custom-pressure').textContent = this.customPressure.toFixed(1) + ' kPa';
        this.debouncedFetch();
      });
    }

    // Ask AI button
    const askBtn = document.getElementById('sim-ask-ai-btn');
    if (askBtn) {
      askBtn.addEventListener('click', () => {
        if (!window.aiAssistant) return;
        const lang = window.i18n ? window.i18n.currentLanguage : 'en';
        const prompt = lang === 'az'
          ? `Hazırkı kosmik missiya ssenarisini izah et: ${this.currentScenario}`
          : `Explain the current mission fire hazard scenario: ${this.currentScenario}`;
        window.aiAssistant.openPanel();
        window.aiAssistant.inputField.value = prompt;
      });
    }

    // Load default scenario
    this.loadScenario('iss');
  }

  selectPreset(scenarioId) {
    this.currentScenario = scenarioId;

    // Update active card UI
    document.querySelectorAll('.preset-card').forEach(c => c.classList.remove('active'));
    const activeCard = document.querySelector(`.preset-card[data-scenario="${scenarioId}"]`);
    if (activeCard) activeCard.classList.add('active');

    // Show/hide custom sliders panel
    const customPanel = document.getElementById('custom-sliders-panel');
    if (customPanel) {
      customPanel.style.display = scenarioId === 'custom' ? 'block' : 'none';
    }

    this.loadScenario(scenarioId);
  }

  debouncedFetch() {
    if (this.debounceTimer) clearTimeout(this.debounceTimer);
    this.debounceTimer = setTimeout(() => this.loadScenario('custom'), 300);
  }

  async loadScenario(scenarioId) {
    const customO2 = scenarioId === 'custom' ? this.customO2 : null;
    const customPressure = scenarioId === 'custom' ? this.customPressure : null;

    const data = await window.apiClient.fetchMissionScenario(scenarioId, customO2, customPressure);
    if (!data) return;

    this.renderScenario(data);

    // Update AI context
    if (window.aiAssistant) {
      window.aiAssistant.setPageContext({
        section: 'Mission Simulator',
        scenario: data.scenario.name_en,
        oxygen_pct: data.metrics.oxygen_pct + '%',
        pressure: data.metrics.pressure_kpa + ' kPa',
        fire_hazard_index: data.fire_hazard_index + '/10',
        risk_level: data.risk_level_en
      });
    }
  }

  renderScenario(data) {
    const lang = window.i18n ? window.i18n.currentLanguage : 'en';
    const m = data.metrics;
    const fhi = data.fire_hazard_index;
    const color = data.status_color;
    const riskLabel = lang === 'az' ? data.risk_level_az : data.risk_level_en;
    const advisory = lang === 'az' ? data.advisory_az : data.advisory_en;

    // FHI Score & label
    const fhiScore = document.getElementById('fhi-score');
    if (fhiScore) {
      fhiScore.textContent = fhi.toFixed(1);
      fhiScore.style.color = color;
    }

    const fhiLabel = document.getElementById('fhi-risk-label');
    if (fhiLabel) {
      fhiLabel.textContent = riskLabel;
      fhiLabel.style.color = color;
    }

    // Gauge bar
    const gauge = document.getElementById('hazard-gauge-fill');
    if (gauge) {
      gauge.style.width = `${(fhi / 10) * 100}%`;
      gauge.style.backgroundColor = color;
      gauge.style.boxShadow = `0 0 12px ${color}60`;
    }

    // Metric values
    const setMetric = (id, val) => {
      const el = document.getElementById(id);
      if (el) el.textContent = val;
    };

    setMetric('sim-o2-val', m.oxygen_pct.toFixed(1) + '%');
    setMetric('sim-pressure-val', m.pressure_kpa.toFixed(1) + ' kPa');
    setMetric('sim-po2-val', m.oxygen_partial_pressure_kpa.toFixed(2) + ' kPa');
    setMetric('sim-de-val', m.projected_extinction_diameter_mm.toFixed(3) + ' mm');
    setMetric('sim-mult-val', m.burn_rate_multiplier.toFixed(2) + '×');
    setMetric('sim-purge-val', m.required_inert_purge_pct.toFixed(1) + '% N₂/CO₂');

    // Scenario name
    const nameEl = document.getElementById('sim-scenario-name');
    if (nameEl) {
      nameEl.textContent = lang === 'az' ? data.scenario.name_az : data.scenario.name_en;
    }

    // Advisory card
    const advEl = document.getElementById('sim-advisory-text');
    if (advEl) advEl.textContent = advisory;
  }
}

window.simulator = new FireXSimulator();
