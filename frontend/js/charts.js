/**
 * NASA FIRE-X Chart.js Visualization Engine
 * High-precision microgravity telemetry rendering
 */

class FireXChartsEngine {
  constructor() {
    this.charts = {};
  }

  init(statsData) {
    if (!statsData) return;

    this.renderExtinctionScatter(statsData.extinction_scatter || []);
    this.renderAirflowBurnChart(statsData.burn_airflow_data || []);
    this.renderFuelMatrixChart(statsData.top_fuels || []);
    this.renderOutcomesChart(statsData.outcomes || []);
  }

  // Chart 1: Extinction Diameter vs Oxygen %
  renderExtinctionScatter(dataPoints) {
    const canvas = document.getElementById('chart-extinction-scatter');
    if (!canvas) return;

    if (this.charts.extinction) this.charts.extinction.destroy();

    const formattedPoints = dataPoints.map(p => ({
      x: p.o2,
      y: p.de,
      meta: p
    }));

    // Regression curve points for reference
    const curvePoints = [];
    for (let o2 = 14; o2 <= 50; o2 += 2) {
      const de = 2.85 * Math.exp(-0.038 * o2);
      curvePoints.push({ x: o2, y: Number(de.toFixed(3)) });
    }

    const ctx = canvas.getContext('2d');
    this.charts.extinction = new Chart(ctx, {
      type: 'scatter',
      data: {
        datasets: [
          {
            label: 'Extinction Limit Curve',
            data: curvePoints,
            type: 'line',
            borderColor: 'rgba(0, 229, 255, 0.8)',
            borderWidth: 2,
            borderDash: [5, 5],
            fill: false,
            pointRadius: 0,
            tension: 0.4
          },
          {
            label: 'NASA Experiments',
            data: formattedPoints,
            backgroundColor: 'rgba(0, 119, 255, 0.75)',
            borderColor: '#00E5FF',
            borderWidth: 1,
            pointRadius: 5,
            pointHoverRadius: 8
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            labels: { color: '#94A3B8', font: { family: 'JetBrains Mono', size: 11 } }
          },
          tooltip: {
            backgroundColor: 'rgba(10, 15, 26, 0.95)',
            titleColor: '#00E5FF',
            bodyColor: '#FFFFFF',
            borderColor: '#1E293B',
            borderWidth: 1,
            callbacks: {
              label: (ctx) => {
                const raw = ctx.raw;
                if (raw.meta) {
                  return [
                    `ID: ${raw.meta.id} (${raw.meta.family})`,
                    `Fuel: ${raw.meta.fuel}`,
                    `O₂: ${raw.x}% | dₑ: ${raw.y} mm`
                  ];
                }
                return `Theoretical Limit: ${raw.y} mm @ ${raw.x}% O₂`;
              }
            }
          }
        },
        scales: {
          x: {
            title: { display: true, text: 'Oxygen Concentration (O₂ %)', color: '#94A3B8', font: { family: 'Inter', size: 11, weight: 600 } },
            grid: { color: 'rgba(255, 255, 255, 0.05)' },
            ticks: { color: '#64748B', font: { family: 'JetBrains Mono' } }
          },
          y: {
            title: { display: true, text: 'Extinction Diameter dₑ (mm)', color: '#94A3B8', font: { family: 'Inter', size: 11, weight: 600 } },
            grid: { color: 'rgba(255, 255, 255, 0.05)' },
            ticks: { color: '#64748B', font: { family: 'JetBrains Mono' } }
          }
        }
      }
    });
  }

  // Chart 2: Burn Time vs Airflow Velocity
  renderAirflowBurnChart(dataPoints) {
    const canvas = document.getElementById('chart-airflow-burn');
    if (!canvas) return;

    if (this.charts.airflow) this.charts.airflow.destroy();

    const formattedPoints = dataPoints.map(p => ({
      x: p.airflow,
      y: p.burn_time,
      meta: p
    }));

    const ctx = canvas.getContext('2d');
    this.charts.airflow = new Chart(ctx, {
      type: 'scatter',
      data: {
        datasets: [
          {
            label: 'Forced Flow Telemetry',
            data: formattedPoints,
            backgroundColor: 'rgba(245, 158, 11, 0.75)',
            borderColor: '#F59E0B',
            borderWidth: 1,
            pointRadius: 5,
            pointHoverRadius: 8
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            labels: { color: '#94A3B8', font: { family: 'JetBrains Mono', size: 11 } }
          },
          tooltip: {
            backgroundColor: 'rgba(10, 15, 26, 0.95)',
            titleColor: '#F59E0B',
            bodyColor: '#FFFFFF',
            borderColor: '#1E293B',
            borderWidth: 1,
            callbacks: {
              label: (ctx) => {
                const m = ctx.raw.meta;
                return [
                  `ID: ${m.id} (${m.family})`,
                  `Airflow: ${ctx.raw.x} cm/s`,
                  `Burn Time: ${ctx.raw.y} s`
                ];
              }
            }
          }
        },
        scales: {
          x: {
            title: { display: true, text: 'Forced Airflow Velocity (cm/s)', color: '#94A3B8', font: { family: 'Inter', size: 11, weight: 600 } },
            grid: { color: 'rgba(255, 255, 255, 0.05)' },
            ticks: { color: '#64748B', font: { family: 'JetBrains Mono' } }
          },
          y: {
            title: { display: true, text: 'Burn Duration (seconds)', color: '#94A3B8', font: { family: 'Inter', size: 11, weight: 600 } },
            grid: { color: 'rgba(255, 255, 255, 0.05)' },
            ticks: { color: '#64748B', font: { family: 'JetBrains Mono' } }
          }
        }
      }
    });
  }

  // Chart 3: Fuel Materials Distribution
  renderFuelMatrixChart(topFuels) {
    const canvas = document.getElementById('chart-fuel-matrix');
    if (!canvas) return;

    if (this.charts.fuels) this.charts.fuels.destroy();

    const labels = topFuels.map(f => f.fuel);
    const counts = topFuels.map(f => f.count);

    const colors = [
      'rgba(0, 229, 255, 0.85)',
      'rgba(0, 119, 255, 0.85)',
      'rgba(16, 185, 129, 0.85)',
      'rgba(245, 158, 11, 0.85)',
      'rgba(239, 68, 68, 0.85)',
      'rgba(168, 85, 247, 0.85)',
      'rgba(236, 72, 153, 0.85)',
      'rgba(20, 184, 166, 0.85)',
      'rgba(249, 115, 22, 0.85)',
      'rgba(100, 116, 139, 0.85)'
    ];

    const ctx = canvas.getContext('2d');
    this.charts.fuels = new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: labels,
        datasets: [
          {
            data: counts,
            backgroundColor: colors,
            borderColor: '#0A0F1A',
            borderWidth: 2,
            hoverOffset: 6
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'right',
            labels: { color: '#94A3B8', font: { family: 'Inter', size: 11 }, boxWidth: 12 }
          }
        },
        cutout: '65%'
      }
    });
  }

  // Chart 4: Extinction Outcomes Distribution
  renderOutcomesChart(outcomes) {
    const canvas = document.getElementById('chart-outcomes');
    if (!canvas) return;

    if (this.charts.outcomes) this.charts.outcomes.destroy();

    const labels = outcomes.map(o => o.outcome);
    const counts = outcomes.map(o => o.count);

    const ctx = canvas.getContext('2d');
    this.charts.outcomes = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [
          {
            label: 'Experiment Count',
            data: counts,
            backgroundColor: 'rgba(0, 229, 255, 0.65)',
            borderColor: '#00E5FF',
            borderWidth: 1,
            borderRadius: 4
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        indexAxis: 'y',
        plugins: {
          legend: { display: false }
        },
        scales: {
          x: {
            grid: { color: 'rgba(255, 255, 255, 0.05)' },
            ticks: { color: '#64748B', font: { family: 'JetBrains Mono' } }
          },
          y: {
            grid: { display: false },
            ticks: { color: '#94A3B8', font: { family: 'Inter', size: 11 } }
          }
        }
      }
    });
  }
}

window.chartsEngine = new FireXChartsEngine();
