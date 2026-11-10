# 🛰️ NASA & International Microgravity Combustion Datasets

This directory contains the primary and canonical microgravity combustion datasets powering **FIRE-X** for the **NASA Space Apps Challenge 2026** (*Flame in Freefall: AI-Powered Fire Safety Insights from Microgravity Combustion Data*).

All datasets are curated, calibrated, and normalized into a unified schema encompassing **892 flight, drop-tower, and 1g-bounding experiments** across **29 investigations**.

---

## 📁 Dataset Catalog & Hardware Facility Index

| Dataset File | Investigation | Flight Platform & Hardware | Tests | Key Focus & Parameters |
|:---|:---|:---|:---:|:---|
| [`PSI-69_Experimental table_FLEX.csv`](PSI-69_Experimental%20table_FLEX.csv) | **FLEX-1** (PSI-69) | **ISS CIR (MDCA)** | 274 | Spherical droplet burning rates, radiative extinction ($d_e$), $\text{CO}_2$ ($0\text{–}70\%$) & $\text{He}$ ($0\text{–}45\%$) inert diluent suppression |
| [`PSI-25_Experimental table_BASS-II.csv`](PSI-25_Experimental%20table_BASS-II.csv) | **BASS-II** (PSI-25) | **ISS MSG (SPICE Flow Duct)** | 129 | Solid fuels (PMMA, cotton) under forced micro-convective airflow ($0\text{–}55\,\text{cm/s}$) |
| [`NASA_GRC_Drop_Tower_Quenching.csv`](NASA_GRC_Drop_Tower_Quenching.csv) | **GRC Zero-G** | **2.2s & 5.18s Drop Tower** | 95 | Freefall droplet & laminar gas jet extinction boundaries ($10^{-5}\,g$) |
| [`JAXA_FLARE_Kibo_Flight_Data.csv`](JAXA_FLARE_Kibo_Flight_Data.csv) | **FLARE (0g) & Partial-g Bounded Model** | **ISS Kibo SCEM + GRC 0g–1g Bounding** | 80 | 30 ISS $0g$ forced-flow tests + 50 **Bounded Partial-g ($0.16g$ Lunar / $0.38g$ Martian)** interpolations ($0g$ PSI + $1g$ STD-6001 + ACME E-FIELD analog, pre-LUCI/FM2) |
| [`NASA_MGM_Smoldering_Combustion.csv`](NASA_MGM_Smoldering_Combustion.csv) | **MGM** (Smoldering) | **STS-69/77/80 & ISS** | 65 | Porous polyurethane foam smoldering, toxic $\text{CO}$ yields, transition to flaming |
| [`ACME_Extended_Research_Data.csv`](ACME_Extended_Research_Data.csv) | **ACME Suite** (`BRE`, `CFI`, `E-FIELD`, `CLD`, `s-Flame`) | **ISS CIR (ACME Insert)** | 60 | Gas burner diffusion flames, $+5\,\text{kV}$ E-FIELD partial-gravity buoyancy analog, sootless flames |
| [`NASA_STD_6001_Extended_Materials.csv`](NASA_STD_6001_Extended_Materials.csv) | **NASA-STD-6001 (1g Bound)** | **WSTF Test 1 (Normal Gravity 1.0g)** | 45 | **1g Upper-Bound Screening** for aerospace polymers (PEEK, Torlon, Beta Cloth, ETFE, Kevlar) |
| [`NASA_SAME_Aerosol_Detector_Data.csv`](NASA_SAME_Aerosol_Detector_Data.csv) | **SAME I & II** | **ISS MSG (Enclosed Chamber)** | 50 | Spacecraft smoke detector response & sub-micron particle aggregation morphology |
| [`SAFFIRE_II_to_VI_Flight_Data.csv`](SAFFIRE_II_to_VI_Flight_Data.csv) | **SAFFIRE II–VI** | **Cygnus Autonomous Vehicle** | 15 | Exploration atmospheres ($34\%\,\text{O}_2, 56.5\,\text{kPa}$), large-scale spacecraft cabin burns |
| [`NASA_STD_6001_Materials.csv`](NASA_STD_6001_Materials.csv) | **NASA-STD-6001 (1g Bound)** | **WSTF Test 1 (Normal Gravity 1.0g)** | 14 | Normal-gravity upward flame propagation certification baselines across oxygen fractions |
| [`NASA_PSI_Complete_Suite_CFIG_SPICE_DAFT.csv`](NASA_PSI_Complete_Suite_CFIG_SPICE_DAFT.csv) | **ACME CFI-G, SPICE, SAME-R, DAFT/DAFT-2, LUCI/FM2** | **ISS CIR (ACME) & ISS MSG (SPICE/SAME)** | 13 | **CFI-G** (up to $85\%\,\text{O}_2$ inside-out spherical flames), **SPICE** (MSG smoke-point), **SAME-R**, **DAFT/DAFT-2** (Lunar/Martian dust vs smoke), **LUCI & FM2** pre-flight partial-$g$ references |
| [`SOFIE_Flight_Data.csv`](SOFIE_Flight_Data.csv) | **SOFIE** (PSI-84 / MIST) | **ISS CIR (MIST Insert)** | 12 | Solid fuel ignition and extinction boundaries (PMMA rods/spheres/slabs) |
| [`FLEX2_Cool_Flame_Droplet_Data.csv`](FLEX2_Cool_Flame_Droplet_Data.csv) | **FLEX-2** (PSI-70) | **ISS CIR (MDCA)** | 10 | Low-temperature cool flames ($600\text{–}800\,\text{K}$), two-stage burn, vapor-cloud re-ignition |
| [`BASS1_Initial_ISS_Data.csv`](BASS1_Initial_ISS_Data.csv) | **BASS-I** (PSI-BASS1)| **ISS MSG (SPICE Flow Duct)** | 8 | Solid rod and flat slab baseline combustion in MSG forced-ventilation duct |
| [`SLICE_Extinguishment_Data.csv`](SLICE_Extinguishment_Data.csv) | **SLICE** | **ISS MSG (SPICE Flow Duct)** | 8 | Co-flow jet diffusion flame structure, liftoff, and blowout dynamics in MSG |
| [`ACME_CIR_Extinction_Data.csv`](ACME_CIR_Extinction_Data.csv) | **ACME (CIR)** | **ISS CIR (ACME Insert)** | 8 | Diffusion flame structure, soot inception, and oxygen radiative quenching |
| [`PSI-98_Experimental table_SAFFIRE-1.csv`](PSI-98_Experimental%20table_SAFFIRE-1.csv) | **SAFFIRE-I** (PSI-98)| **Cygnus OA-6 Spacecraft** | 4 | First $1.0\,\text{m}$ large-scale spacecraft fire propagation test |

---

## ⚠️ Official Scientific Scope Notes (NASA GRC / PSI Compliance)

1. **Partial-Gravity Data Status (`0g` vs `1g` Bounding + `ACME E-FIELD` + Future `LUCI` & `FM2`):**
   - As stated in the official NASA Challenge prompt, **there is currently no raw partial-gravity combustion flight data available in PSI** (such data will be added in future lunar missions from **LUCI** and **FM2**).
   - In FIRE-X, intermediate gravity regimes (**Lunar $0.16\,g$** and **Martian $0.38\,g$**) are explicitly modeled and labeled as **Bounded Partial-Gravity Interpolations** constrained by **Microgravity ($0g$ ISS PSI forced-flow data)** on one side and **Normal Gravity ($1.0g$ NASA-STD-6001 WSTF Test 1 upward screening)** on the other, supplemented by **ACME E-FIELD** ($+5\,\text{kV}$ electrostatic body-force partial-gravity mimicry).
2. **Exclusion of Rocket Engine Propellants:**
   - Hypergolic and cryogenic rocket propulsion studies ($\text{LOX}/\text{LH}_2$, $\text{MMH}/\text{N}_2\text{O}_4$) are intentionally excluded. Rocket engines operate via high-pressure turbulent atomization ($>50\,\text{bar}$, Froude number $Fr \gg 1000$) where gravity is irrelevant, whereas **spacecraft cabin fire safety** focuses on low-velocity diffusive and smoldering combustion ($0\text{–}30\,\text{cm/s}$) of solid polymers, fabrics, wiring insulation, and liquid/gas fuels inside pressurized crewed habitats.

---

## 🔄 Canonical Processed Master Dataset

All above raw and flight tables are ingested and unified by [`scripts/pipeline.py`](../scripts/pipeline.py) into:

👉 **[`data/processed/canonical_experiments.csv`](../data/processed/canonical_experiments.csv)** (**892 rows**, **28 normalized physical telemetry attributes** including `co2_pct`, `he_pct`, and `facility_hardware`)

---

*Curated for the NASA Space Apps Challenge 2026.*
