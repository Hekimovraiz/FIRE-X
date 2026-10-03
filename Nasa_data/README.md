# 🛰️ NASA & International Microgravity Combustion Datasets

This directory contains the primary and canonical microgravity combustion datasets powering **FIRE-X** for the **NASA Space Apps Challenge 2026** (*Flame in Freefall: AI-Powered Fire Safety Insights from Microgravity Combustion Data*).

All datasets are curated, calibrated, and normalized into a unified schema encompassing **879 flight and drop-tower experiments** across **24 investigations**.

---

## 📁 Dataset Catalog & File Index

| Dataset File | Investigation | Flight Platform | Tests | Key Focus & Parameters |
|:---|:---|:---|:---:|:---|
| [`PSI-69_Experimental table_FLEX.csv`](PSI-69_Experimental%20table_FLEX.csv) | **FLEX-1** (PSI-69) | ISS CIR | 274 | Spherical droplet burning rates, radiative extinction, $d_e$, alkane fuels |
| [`PSI-25_Experimental table_BASS-II.csv`](PSI-25_Experimental%20table_BASS-II.csv) | **BASS-II** (PSI-25) | ISS MSG | 129 | Solid fuels (PMMA, cotton) under forced micro-convective airflow |
| [`NASA_GRC_Drop_Tower_Quenching.csv`](NASA_GRC_Drop_Tower_Quenching.csv) | **GRC Zero-G** | 2.2s & 5.18s Tower | 95 | Freefall droplet & laminar gas jet extinction boundaries ($10^{-5}\,g$) |
| [`JAXA_FLARE_Kibo_Flight_Data.csv`](JAXA_FLARE_Kibo_Flight_Data.csv) | **FLARE** (JAXA/Kibo) | ISS Kibo MSPR | 80 | Reduced-gravity flammability: Lunar ($0.16\,g$) & Martian ($0.38\,g$) limits |
| [`NASA_MGM_Smoldering_Combustion.csv`](NASA_MGM_Smoldering_Combustion.csv) | **MGM** (Smoldering) | STS-69/77/80 & ISS | 65 | Porous polymer foam smoldering, toxic CO yields, transition to flaming |
| [`ACME_Extended_Research_Data.csv`](ACME_Extended_Research_Data.csv) | **ACME Extended** | ISS CIR | 60 | BRE, CFI coflow, E-FIELD ($+5\,\text{kV}$ ionic wind), CLD sootless flames |
| [`NASA_STD_6001_Extended_Materials.csv`](NASA_STD_6001_Extended_Materials.csv) | **NASA-STD-6001** | WSTF Test 1 & 2 | 45 | High-performance aerospace polymers (PEEK, Torlon, Beta Cloth, ETFE) |
| [`NASA_SAME_Aerosol_Detector_Data.csv`](NASA_SAME_Aerosol_Detector_Data.csv) | **SAME I & II** | ISS MSG | 50 | Spacecraft smoke detector response & sub-micron particle morphology |
| [`SAFFIRE_II_to_VI_Flight_Data.csv`](SAFFIRE_II_to_VI_Flight_Data.csv) | **SAFFIRE II–VI** | Cygnus Orbital | 15 | Exploration atmospheres ($34\%\,O_2, 56.5\,\text{kPa}$), large-scale burns |
| [`NASA_STD_6001_Materials.csv`](NASA_STD_6001_Materials.csv) | **NASA-STD-6001** | WSTF | 14 | Upward flame propagation certification tests across oxygen fractions |
| [`SOFIE_Flight_Data.csv`](SOFIE_Flight_Data.csv) | **SOFIE** (PSI-84) | ISS CIR | 12 | Solid fuel ignition and extinction boundaries |
| [`FLEX2_Cool_Flame_Droplet_Data.csv`](FLEX2_Cool_Flame_Droplet_Data.csv) | **FLEX-2** (PSI-70) | ISS CIR | 10 | Low-temperature cool flames, second-stage burn, invisible extinction |
| [`BASS1_Initial_ISS_Data.csv`](BASS1_Initial_ISS_Data.csv) | **BASS-I** (PSI-BASS1)| ISS MSG | 8 | Solid rod and flat slab baseline combustion in ventilation ducts |
| [`SLICE_Extinguishment_Data.csv`](SLICE_Extinguishment_Data.csv) | **SLICE** | ISS CIR | 8 | Inert gas ($CO_2, N_2$) jet flame suppression and liftoff dynamics |
| [`ACME_CIR_Extinction_Data.csv`](ACME_CIR_Extinction_Data.csv) | **ACME (CIR)** | ISS CIR | 8 | Diffusion flame structure, soot inception, and oxygen quenching |
| [`PSI-98_Experimental table_SAFFIRE-1.csv`](PSI-98_Experimental%20table_SAFFIRE-1.csv) | **SAFFIRE-I** (PSI-98)| Cygnus OA-6 | 4 | First $1.0\,\text{m}$ large-scale spacecraft fire test |

---

## 🔄 Canonical Processed Master Dataset

All above raw and flight tables are ingested and unified by [`scripts/pipeline.py`](../scripts/pipeline.py) into:

👉 **[`data/processed/canonical_experiments.csv`](../data/processed/canonical_experiments.csv)** (879 rows, 26 normalized physical telemetry attributes)

### Normalized Telemetry Schema:
1. `experiment_id` — Unique identifier (e.g., `FLEX-042`, `FLARE-KIBO-012`, `MGM-ISS-005`)
2. `dataset_family` — Flight investigation suite (FLEX, BASS, FLARE, MGM, SAFFIRE, etc.)
3. `investigation_id` — Official NASA PSI / Mission identifier
4. `fuel_material` — Chemical or trade name (e.g., `n-Heptane`, `PMMA`, `Nomex HT90-40`)
5. `material_category` — Material typology (Liquid Droplet, Solid Polymer, Aramid, Porous Foam)
6. `oxygen_pct` — Ambient oxygen concentration ($12.0\% - 40.0\%$)
7. `pressure_kpa` — Ambient atmospheric pressure ($50.0 - 150.0\,\text{kPa}$)
8. `burn_time_s` — Duration of active combustion (seconds)
9. `extinction_outcome` — Quenching regime (Radiative Quenching, Convective Blowoff, Smolder Extinction)
10. `extinction_diameter_mm` — Droplet or sample extinction dimension ($d_e$)
11. `initial_diameter_mm` — Sample initial size ($d_0$)
12. `burning_rate_mms` — Regressing burning rate ($K$ or $r_b$ in $\text{mm/s}$)
13. `airflow_velocity_cms` — Forced convective airflow velocity ($0.0 - 35.0\,\text{cm/s}$)
14. `flame_temp_k` — Measured/inferred flame temperature ($\text{K}$)
15. `gravity_condition` — Gravitational field (Microgravity, Lunar $0.16g$, Martian $0.38g$, Earth $1g$)
16. `ignition_power_w` / `ignition_time_s` — Ignition spark or hot-wire electrical energy
17. `co2_pct` / `co_ppm` — Combustion byproduct and toxic emission measurements
18. `source_name` / `source_url` — NASA Physical Sciences Informatics (PSI) citation & permalink
19. `notes` — Physical observation logs from flight payload specialists and PIs

---

*Curated for the NASA Space Apps Challenge 2026 by Team FIRE-X.*
