/**
 * NASA FIRE-X API Client
 * Secure communication layer for platform telemetry, analytics, and AI assistant
 */

class FireXApiClient {
  constructor() {
    this.baseUrl = '';
  }

  async fetchStats() {
    try {
      const res = await fetch(`${this.baseUrl}/api/stats`);
      const data = await res.json();
      return data.success ? data.data : null;
    } catch (e) {
      console.error('Error fetching platform stats:', e);
      return null;
    }
  }

  async fetchExperiments(params = {}) {
    try {
      const url = new URL(`${window.location.origin}/api/experiments`);
      Object.keys(params).forEach(k => {
        if (params[k] !== undefined && params[k] !== null && params[k] !== '') {
          url.searchParams.append(k, params[k]);
        }
      });
      const res = await fetch(url);
      const data = await res.json();
      return data.success ? data.data : { experiments: [], total: 0 };
    } catch (e) {
      console.error('Error querying experiments:', e);
      return { experiments: [], total: 0 };
    }
  }

  async fetchExperimentById(id) {
    try {
      const res = await fetch(`${this.baseUrl}/api/experiments/${encodeURIComponent(id)}`);
      const data = await res.json();
      return data.success ? data.data : null;
    } catch (e) {
      console.error(`Error fetching experiment ${id}:`, e);
      return null;
    }
  }

  async compareExperiments(experimentIds) {
    try {
      const res = await fetch(`${this.baseUrl}/api/compare`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ experiment_ids: experimentIds })
      });
      const data = await res.json();
      return data.success ? data.data : null;
    } catch (e) {
      console.error('Error comparing experiments:', e);
      return null;
    }
  }

  async fetchMissionScenario(scenarioId, customO2 = null, customPressure = null) {
    try {
      const url = new URL(`${window.location.origin}/api/mission-scenario/${scenarioId}`);
      if (customO2 !== null) url.searchParams.append('custom_o2', customO2);
      if (customPressure !== null) url.searchParams.append('custom_pressure', customPressure);
      const res = await fetch(url);
      const data = await res.json();
      return data.success ? data.data : null;
    } catch (e) {
      console.error(`Error fetching scenario ${scenarioId}:`, e);
      return null;
    }
  }

  async sendChatMessage(messages, language = 'en', pageContext = null) {
    try {
      const res = await fetch(`${this.baseUrl}/api/chat-assistant`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          messages: messages,
          language: language,
          page_context: pageContext
        })
      });
      return await res.json();
    } catch (e) {
      console.error('Error communicating with AI assistant:', e);
      return {
        success: false,
        response: language === 'az' 
          ? "Şəbəkə xətası baş verdi. Zəhmət olmasa bir az sonra yenidən cəhd edin." 
          : "Network communication error. Please try again shortly."
      };
    }
  }
}

window.apiClient = new FireXApiClient();
