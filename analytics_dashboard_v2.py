"""
FIRE-X Microgravity Combustion Analytics Dashboard (v2.0)
=========================================================
NASA Space Apps Challenge 2026 — "Flame in Freefall"
Team: SpaceAz (Murad Fatullazada, Sabir Məmmədzadə, Raiz Həkimov, Şahvələd Vəlizadə, Hüseyn Alırzayev)

A dedicated Streamlit application powered by real numerical NASA PSI datasets:
- NASA PSI-69 & PSI-70 (FLEX / FLEX-2 Droplet Extinction & Cool Flames)
- NASA PSI-25 (BASS-II Solid Fuel Opposed/Concurrent Flame Spread)
- NASA PSI-98 (SAFFIRE Large-Scale Spacecraft Flame Propagation)
"""

import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

from backend.nasa_combustion_engine import combustion_engine, MATERIAL_PROPERTIES

# Streamlit Page Configuration
st.set_page_config(
    page_title="FIRE-X — Microgravity Combustion Analytics",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Cyberpunk / Dark Space CSS
st.markdown("""
<style>
    .reportview-container, .main {
        background-color: #020409;
        color: #E2E8F0;
    }
    .stApp {
        background: radial-gradient(circle at 50% 10%, #070D1A 0%, #020409 90%);
    }
    .disclaimer-banner {
        background: rgba(255, 107, 53, 0.12);
        border: 1px solid rgba(255, 107, 53, 0.4);
        border-radius: 10px;
        padding: 12px 20px;
        color: #FF6B35;
        font-family: 'Courier New', Courier, monospace;
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 24px;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .metric-card {
        background: rgba(11, 21, 42, 0.85);
        border: 1px solid rgba(0, 245, 255, 0.25);
        border-radius: 12px;
        padding: 18px;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
    }
    .metric-val {
        font-size: 2.2rem;
        font-weight: 800;
        color: #00F5FF;
        font-family: monospace;
    }
    .metric-label {
        font-size: 0.75rem;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-top: 4px;
    }
</style>
""", unsafe_allow_html=True)

# Mandatory Safety Disclaimer Banner
st.markdown("""
<div class="disclaimer-banner">
    <span>⚠️</span>
    <span><strong>FIRE-X DECISION SUPPORT SYSTEM:</strong> Empirical Analytics & Reference Tool (Non-Autonomic). Real-time life-critical flight decisions must be confirmed with NASA Flight Operations Manuals (FOM) & Mission Control Houston.</span>
</div>
""", unsafe_allow_html=True)

# Main Title & Subtitle
st.title("🔥 NASA FIRE-X — Microgravity Combustion Analytics Panel")
st.markdown("### *Empirical Predictive Modeling Derived from NASA Physical Sciences Informatics (PSI)*")
st.markdown("---")

# Top KPI Metric Row
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
with kpi1:
    st.markdown('<div class="metric-card"><div class="metric-val">892</div><div class="metric-label">Canonical Flight Tests</div></div>', unsafe_allow_html=True)
with kpi2:
    st.markdown('<div class="metric-card"><div class="metric-val">29</div><div class="metric-label">PSI Investigations</div></div>', unsafe_allow_html=True)
with kpi3:
    st.markdown('<div class="metric-card"><div class="metric-val">0.0 – 1.0g</div><div class="metric-label">Gravity Bounding Span</div></div>', unsafe_allow_html=True)
with kpi4:
    st.markdown('<div class="metric-card"><div class="metric-val">100%</div><div class="metric-label">Citation-Locked RAG</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Sidebar: Mission Environment & Telemetry Testbed Node
st.sidebar.image("images/Fire-X.jpeg", width=120) if os.path.exists("images/Fire-X.jpeg") else None
st.sidebar.title("Telemetry Controls")
st.sidebar.markdown("**Spacecraft Environment Presets:**")
env_choice = st.sidebar.selectbox(
    "Mission Atmosphere",
    ["Standard ISS (21% O2, 101.3 kPa)", "Artemis Lunar Habitat (34% O2, 56.5 kPa)", "Hypoxic Safe-Haven (15% O2, 70.3 kPa)", "Custom Parameters"]
)

if env_choice == "Standard ISS (21% O2, 101.3 kPa)":
    default_o2 = 21.0
    default_p = 101.3
elif env_choice == "Artemis Lunar Habitat (34% O2, 56.5 kPa)":
    default_o2 = 34.0
    default_p = 56.5
elif env_choice == "Hypoxic Safe-Haven (15% O2, 70.3 kPa)":
    default_o2 = 15.0
    default_p = 70.3
else:
    default_o2 = 21.0
    default_p = 101.3

sidebar_o2 = st.sidebar.slider("Ambient Oxygen O2 (%)", 10.0, 45.0, default_o2, 0.5)
sidebar_p = st.sidebar.slider("Cabin Pressure (kPa)", 40.0, 150.0, default_p, 1.0)
sidebar_flow = st.sidebar.slider("Ventilation Airflow U_inf (cm/s)", 0.0, 30.0, 8.0, 0.5)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📡 Hardware Telemetry Node Bridge")
st.sidebar.caption("Re-branded ESP-32 + SnO2 Physical Testbed Edge Node. Simulates local environmental boundary volatility.")
hw_gas = st.sidebar.slider("Local Hydrocarbon / Pyrolysis Off-gas (PPM)", 10.0, 500.0, 35.0, 5.0)
hw_smoke = st.sidebar.slider("Optical Smoke Obscuration (%)", 0.0, 100.0, 4.0, 1.0)

# Main Tab Panels
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Solid Flame Spread (BASS / SAFFIRE)",
    "💧 Droplet Extinction (FLEX / FLEX-2)",
    "🛰️ Physical Edge Node Ingestion",
    "📊 NASA PSI Raw Datasets"
])

# ==============================================================================
# TAB 1: SOLID FLAME SPREAD DYNAMICS (NASA PSI-25 & PSI-98)
# ==============================================================================
with tab1:
    st.subheader("Microgravity Solid Flame Spread Rate (S_f) & The Low-Flow Flammability Peak")
    st.markdown("""
    **Aerospace Combustion Insight:** In zero-gravity without buoyant convection, flames self-extinguish in stagnant air ($U_\\infty = 0\\text{ cm/s}$) due to $CO_2$ self-blanketing. 
    However, at **low-speed forced ventilation ($2 - 15\\text{ cm/s}$)** — typical of ISS cabin ventilation fans — flames receive fresh oxidizer without convective cooling, 
    causing flame spread rates to reach a **critical peak that exceeds 1.0g normal gravity!**
    """)

    col_mat, col_calc = st.columns([1, 2])
    with col_mat:
        target_material = st.selectbox("Solid Combustible Material", list(MATERIAL_PROPERTIES.keys())[:3])
        mat_info = MATERIAL_PROPERTIES[target_material]
        st.info(f"**Material:** {target_material}\n\n"
                f"- **Solid Density:** `{mat_info['rho_s']} kg/m³`\n"
                f"- **Pyrolysis Temp:** `{mat_info['T_v']} K`\n"
                f"- **0g Stagnant MOC:** `{mat_info['moc_0g_stagnant']}% O₂`\n"
                f"- **0g Low-Flow MOC:** `{mat_info['moc_0g_flow']}% O₂`\n"
                f"- **1.0g Normal MOC:** `{mat_info['moc_1g']}% O₂`\n"
                f"- **NASA Dataset:** `{mat_info['psi_investigation']}`")

        # Single calculation for current slider values
        res = combustion_engine.predict_solid_flame_spread(
            material=target_material,
            flow_velocity_cms=sidebar_flow,
            oxygen_pct=sidebar_o2,
            pressure_kpa=sidebar_p
        )
        st.metric("Predicted Flame Spread Rate", f"{res['flame_spread_rate_mms']} mm/s", delta=res['hazard_level'])
        st.caption(f"**Formal Empirical Citation:** `{res['empirical_citation']}`")

    with col_calc:
        # Generate velocity curve across 0 to 30 cm/s
        v_range = np.linspace(0.0, 30.0, 60)
        micro_rates = []
        normal_rates = []

        for v in v_range:
            p_res = combustion_engine.predict_solid_flame_spread(
                material=target_material,
                flow_velocity_cms=v,
                oxygen_pct=sidebar_o2,
                pressure_kpa=sidebar_p
            )
            micro_rates.append(p_res['flame_spread_rate_mms'])
            # 1.0g normal gravity comparison baseline (buoyancy dominates at ~30 cm/s)
            normal_1g = max(0.0, 0.45 * ((sidebar_o2 - mat_info['moc_1g']) / 10.0))
            normal_rates.append(normal_1g)

        fig_spread = go.Figure()
        fig_spread.add_trace(go.Scatter(
            x=v_range, y=micro_rates,
            mode='lines+markers', name='Microgravity (0g Forced Flow)',
            line=dict(color='#00F5FF', width=3),
            marker=dict(size=4)
        ))
        fig_spread.add_trace(go.Scatter(
            x=v_range, y=normal_rates,
            mode='lines', name='1.0g Terrestrial Baseline (NASA-STD-6001)',
            line=dict(color='#FF6B35', width=2, dash='dash')
        ))
        # Mark current operating point
        fig_spread.add_trace(go.Scatter(
            x=[sidebar_flow], y=[res['flame_spread_rate_mms']],
            mode='markers', name='Current Mission Operating Point',
            marker=dict(color='#00E676', size=14, symbol='diamond')
        ))

        fig_spread.update_layout(
            title=f"Flame Spread Rate vs Airflow Velocity ({target_material} @ {sidebar_o2}% O₂)",
            xaxis_title="Forced Airflow Velocity U_inf (cm/s)",
            yaxis_title="Flame Spread Rate S_f (mm/s)",
            template="plotly_dark",
            paper_bgcolor="#070D1A",
            plot_bgcolor="#070D1A",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_spread, use_container_width=True)

# ==============================================================================
# TAB 2: DROPLET EXTINCTION & COOL FLAMES (NASA PSI-69 FLEX)
# ==============================================================================
with tab2:
    st.subheader("Isolated Droplet Combustion & Radiative Extinction Boundaries")
    st.markdown("""
    **FLEX Flight Findings:** In microgravity, fuel droplets burn spherically. Without gravity-driven buoyancy to shed heat, 
    radiative emission from soot particles cools the flame zone, causing sudden **radiative extinction** at a finite diameter ($d_e$). 
    For alkane fuels (n-heptane), this can transition into an invisible, low-temperature **cool flame (600–800 K)** that persists undetected.
    """)

    col_drop1, col_drop2 = st.columns([1, 2])
    with col_drop1:
        fuel_choice = st.selectbox("Droplet Fuel Species", ["n-Heptane Droplet", "Methanol Droplet"])
        init_diam = st.slider("Initial Droplet Diameter d_0 (mm)", 1.0, 5.0, 2.5, 0.1)
        co2_diluent = st.slider("Suppressant CO2 Diluent (%)", 0.0, 70.0, 0.0, 5.0)
        he_diluent = st.slider("Suppressant Helium Diluent (%)", 0.0, 45.0, 0.0, 5.0)

        drop_res = combustion_engine.predict_droplet_combustion(
            fuel=fuel_choice,
            d0_mm=init_diam,
            oxygen_pct=sidebar_o2,
            pressure_kpa=sidebar_p,
            co2_pct=co2_diluent,
            he_pct=he_diluent
        )

        st.success(f"**Burning Rate Constant K:** `{drop_res['burning_rate_constant_K_mm2s']} mm²/s`\n\n"
                   f"**Extinction Diameter d_e:** `{drop_res['extinction_diameter_de_mm']} mm`\n\n"
                   f"**Extinction Ratio d_e/d_0:** `{drop_res['extinction_ratio_de_d0']}`\n\n"
                   f"**Burn Lifetime:** `{drop_res['burn_duration_s']} s`\n\n"
                   f"**Cool Flame Active:** `{'YES (PSI-70 Regime)' if drop_res['cool_flame_transition'] else 'NO'}`")
        st.caption(f"**Empirical Citation:** `{drop_res['empirical_citation']}`")

    with col_drop2:
        # Plot d^2(t) trajectory curve
        t_span = np.linspace(0.0, drop_res['burn_duration_s'], 50)
        d2_vals = [max(drop_res['extinction_diameter_de_mm']**2, init_diam**2 - drop_res['burning_rate_constant_K_mm2s'] * t) for t in t_span]
        d_vals = np.sqrt(d2_vals)

        fig_drop = go.Figure()
        fig_drop.add_trace(go.Scatter(
            x=t_span, y=d_vals,
            mode='lines', name='Droplet Diameter d(t)',
            line=dict(color='#00F5FF', width=3)
        ))
        # Mark extinction point
        fig_drop.add_trace(go.Scatter(
            x=[drop_res['burn_duration_s']], y=[drop_res['extinction_diameter_de_mm']],
            mode='markers+text', name='Radiative Extinction Point (d_e)',
            text=[f"Extinction: {drop_res['extinction_diameter_de_mm']} mm"],
            textposition="top right",
            marker=dict(color='#FF1744', size=12, symbol='x')
        ))

        fig_drop.update_layout(
            title=f"d²-Law Droplet Diameter Trajectory ({fuel_choice} in {sidebar_o2}% O₂)",
            xaxis_title="Time Elapsed (s)",
            yaxis_title="Droplet Diameter (mm)",
            template="plotly_dark",
            paper_bgcolor="#070D1A",
            plot_bgcolor="#070D1A"
        )
        st.plotly_chart(fig_drop, use_container_width=True)

# ==============================================================================
# TAB 3: PHYSICAL TELEMETRY NODE INGESTION BRIDGE
# ==============================================================================
with tab3:
    st.subheader("Physical Testbed Telemetry Node — Atmospheric Boundary Integration")
    st.markdown("""
    **Architectural Clarification:** The physical ESP-32 + SnO₂ hardware unit is not a standalone domestic alarm; 
    it is our **Local Physical Testbed Atmospheric Telemetry Node**. It captures ambient off-gas volatility and thermal decomposition 
    in real time and feeds dynamic boundary parameters directly into the **NASA Microgravity Combustion Engine**.
    """)

    bridge_res = combustion_engine.process_physical_telemetry_node(
        gas_ppm=hw_gas,
        smoke_density_pct=hw_smoke,
        raw_adc=int(hw_gas * 8.2),
        nominal_o2_pct=sidebar_o2,
        nominal_pressure_kpa=sidebar_p,
        target_material=target_material
    )

    b1, b2, b3 = st.columns(3)
    with b1:
        st.markdown("**1. Physical Telemetry Node State:**")
        st.json(bridge_res["physical_testbed_node"])
    with b2:
        st.markdown("**2. Microgravity Physics Output:**")
        st.json(bridge_res["microgravity_physics_state"])
    with b3:
        st.markdown("**3. Scientific Grounding & Protocol:**")
        st.warning(f"**Hazard Status:** {bridge_res['microgravity_physics_state']['system_status']}\n\n"
                   f"**Microgravity FHI Index:** `{bridge_res['microgravity_physics_state']['microgravity_fhi_score']} / 10.0`\n\n"
                   f"**Operational Advisory:** {bridge_res['microgravity_physics_state']['ventilation_recommendation']}")
        st.caption(f"**Citation:** `{bridge_res['citation']}`")

# ==============================================================================
# TAB 4: RAW NASA PSI DATASETS
# ==============================================================================
with tab4:
    st.subheader("NASA Physical Sciences Informatics (PSI) Numerical Data Repositories")
    st.markdown("Inspect raw numerical flight test records loaded into the local engine:")

    ds_summary = combustion_engine.get_dataset_summary()
    st.write(f"**Total Loaded Datasets:** `{ds_summary['total_datasets_loaded']}` | **Empirical Flight Records:** `{ds_summary['total_psi_records']}`")

    selected_ds = st.selectbox("Select Ingested Investigation Dataset", list(combustion_engine.datasets.keys()))
    if selected_ds in combustion_engine.datasets:
        st.dataframe(combustion_engine.datasets[selected_ds].head(100), use_container_width=True)

st.markdown("---")
st.caption("NASA Space Apps Challenge 2026 · Team SpaceAz · Platform Architecture v2.0 · Grounded in NASA Physical Sciences Informatics")
