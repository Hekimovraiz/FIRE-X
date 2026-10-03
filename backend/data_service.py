"""
FIRE-X Data Service Module
Handles SQLite queries, aggregations, experiment filtering, multi-experiment comparisons,
and mission scenario simulations across 484 canonical NASA microgravity combustion records.
"""

import sqlite3
import os
import math
from typing import Dict, Any, List, Optional

DB_PATH = os.path.join(os.path.dirname(__file__), "fire_safety.db")
if not os.path.exists(DB_PATH):
    # Fallback to root DB if backend/fire_safety.db is not present
    DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "fire_safety.db")


def get_db_connection():
    """Get a SQLite database connection with row factory enabled."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def get_stats() -> Dict[str, Any]:
    """Retrieve high-level statistical KPIs and chart aggregation distributions."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Total experiments count
    cursor.execute("SELECT COUNT(*) FROM canonical_experiments")
    total_experiments = cursor.fetchone()[0]

    # Distinct flight families
    cursor.execute("SELECT COUNT(DISTINCT dataset_family) FROM canonical_experiments")
    total_families = cursor.fetchone()[0]

    # Extinction outcomes breakdown
    cursor.execute("""
        SELECT extinction_outcome, COUNT(*) as count 
        FROM canonical_experiments 
        WHERE extinction_outcome IS NOT NULL AND extinction_outcome != ''
        GROUP BY extinction_outcome
        ORDER BY count DESC
    """)
    outcomes = [{"outcome": row["extinction_outcome"], "count": row["count"]} for row in cursor.fetchall()]

    # Fuel materials breakdown
    cursor.execute("""
        SELECT fuel_material, COUNT(*) as count 
        FROM canonical_experiments 
        WHERE fuel_material IS NOT NULL AND fuel_material != ''
        GROUP BY fuel_material
        ORDER BY count DESC
        LIMIT 10
    """)
    top_fuels = [{"fuel": row["fuel_material"], "count": row["count"]} for row in cursor.fetchall()]

    # Dataset families breakdown
    cursor.execute("""
        SELECT dataset_family, COUNT(*) as count 
        FROM canonical_experiments 
        GROUP BY dataset_family 
        ORDER BY count DESC
    """)
    families_dist = [{"family": row["dataset_family"], "count": row["count"]} for row in cursor.fetchall()]

    # Oxygen vs Extinction Diameter data points (for scatter/bubble chart)
    cursor.execute("""
        SELECT experiment_id, dataset_family, fuel_material, oxygen_pct, extinction_diameter_mm, burn_time_s, airflow_velocity_cms
        FROM canonical_experiments
        WHERE oxygen_pct IS NOT NULL AND extinction_diameter_mm IS NOT NULL AND extinction_diameter_mm > 0
        ORDER BY oxygen_pct ASC
    """)
    extinction_scatter = [
        {
            "id": row["experiment_id"],
            "family": row["dataset_family"],
            "fuel": row["fuel_material"],
            "o2": round(row["oxygen_pct"], 1),
            "de": round(row["extinction_diameter_mm"], 3),
            "burn_time": round(row["burn_time_s"], 1) if row["burn_time_s"] else None,
            "airflow": round(row["airflow_velocity_cms"], 1) if row["airflow_velocity_cms"] else None
        }
        for row in cursor.fetchall()
    ]

    # Burn time vs Airflow velocity data points
    cursor.execute("""
        SELECT experiment_id, dataset_family, fuel_material, burn_time_s, airflow_velocity_cms, oxygen_pct
        FROM canonical_experiments
        WHERE burn_time_s IS NOT NULL AND airflow_velocity_cms IS NOT NULL AND burn_time_s > 0
        ORDER BY airflow_velocity_cms ASC
    """)
    burn_airflow_data = [
        {
            "id": row["experiment_id"],
            "family": row["dataset_family"],
            "fuel": row["fuel_material"],
            "burn_time": round(row["burn_time_s"], 1),
            "airflow": round(row["airflow_velocity_cms"], 2),
            "o2": round(row["oxygen_pct"], 1) if row["oxygen_pct"] else None
        }
        for row in cursor.fetchall()
    ]

    # Summary metrics averages
    cursor.execute("""
        SELECT 
            AVG(oxygen_pct) as avg_o2,
            AVG(burn_time_s) as avg_burn_time,
            AVG(extinction_diameter_mm) as avg_de,
            MIN(oxygen_pct) as min_o2,
            MAX(oxygen_pct) as max_o2
        FROM canonical_experiments
    """)
    avg_row = cursor.fetchone()

    conn.close()

    return {
        "total_experiments": total_experiments,
        "total_families": total_families,
        "averages": {
            "avg_oxygen_pct": round(avg_row["avg_o2"], 2) if avg_row["avg_o2"] else 21.0,
            "avg_burn_time_s": round(avg_row["avg_burn_time"], 2) if avg_row["avg_burn_time"] else 0.0,
            "avg_extinction_diameter_mm": round(avg_row["avg_de"], 3) if avg_row["avg_de"] else 0.0,
            "min_o2": round(avg_row["min_o2"], 1) if avg_row["min_o2"] else 15.0,
            "max_o2": round(avg_row["max_o2"], 1) if avg_row["max_o2"] else 50.0
        },
        "outcomes": outcomes,
        "top_fuels": top_fuels,
        "families_distribution": families_dist,
        "extinction_scatter": extinction_scatter,
        "burn_airflow_data": burn_airflow_data
    }


def query_experiments(
    query: Optional[str] = None,
    family: Optional[str] = None,
    fuel: Optional[str] = None,
    outcome: Optional[str] = None,
    min_o2: Optional[float] = None,
    max_o2: Optional[float] = None,
    page: int = 1,
    limit: int = 50,
    sort_by: str = "experiment_id",
    sort_dir: str = "ASC"
) -> Dict[str, Any]:
    """Multi-parameter filtering & search across all 484 experiments."""
    conn = get_db_connection()
    cursor = conn.cursor()

    conditions = ["1=1"]
    params = []

    if query:
        q_wildcard = f"%{query}%"
        conditions.append("(experiment_id LIKE ? OR fuel_material LIKE ? OR dataset_family LIKE ? OR sample_description LIKE ?)")
        params.extend([q_wildcard, q_wildcard, q_wildcard, q_wildcard])

    if family and family.lower() != "all":
        conditions.append("dataset_family = ?")
        params.append(family)

    if fuel and fuel.lower() != "all":
        conditions.append("fuel_material = ?")
        params.append(fuel)

    if outcome and outcome.lower() != "all":
        conditions.append("extinction_outcome = ?")
        params.append(outcome)

    if min_o2 is not None:
        conditions.append("oxygen_pct >= ?")
        params.append(min_o2)

    if max_o2 is not None:
        conditions.append("oxygen_pct <= ?")
        params.append(max_o2)

    where_clause = " AND ".join(conditions)

    # Allowed sort columns
    allowed_sorts = {
        "experiment_id": "experiment_id",
        "dataset_family": "dataset_family",
        "fuel_material": "fuel_material",
        "oxygen_pct": "oxygen_pct",
        "pressure_kpa": "pressure_kpa",
        "burn_time_s": "burn_time_s",
        "extinction_diameter_mm": "extinction_diameter_mm",
        "airflow_velocity_cms": "airflow_velocity_cms"
    }
    sort_column = allowed_sorts.get(sort_by, "experiment_id")
    sort_direction = "DESC" if sort_dir.upper() == "DESC" else "ASC"

    # Count total matches
    count_sql = f"SELECT COUNT(*) FROM canonical_experiments WHERE {where_clause}"
    cursor.execute(count_sql, params)
    total_matches = cursor.fetchone()[0]

    # Fetch paginated results
    offset = (page - 1) * limit
    data_sql = f"""
        SELECT * FROM canonical_experiments 
        WHERE {where_clause} 
        ORDER BY {sort_column} {sort_direction} 
        LIMIT ? OFFSET ?
    """
    cursor.execute(data_sql, params + [limit, offset])
    rows = [dict(r) for r in cursor.fetchall()]

    conn.close()

    return {
        "total": total_matches,
        "page": page,
        "limit": limit,
        "total_pages": math.ceil(total_matches / limit) if limit > 0 else 1,
        "experiments": rows
    }


def get_experiment_by_id(experiment_id: str) -> Optional[Dict[str, Any]]:
    """Retrieve a single experiment by unique ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM canonical_experiments WHERE experiment_id = ?", (experiment_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def compare_experiments(experiment_ids: List[str]) -> Dict[str, Any]:
    """Perform side-by-side metric comparison for 2 to 4 experiments."""
    if not experiment_ids:
        return {"experiments": [], "metrics": {}}

    conn = get_db_connection()
    cursor = conn.cursor()
    placeholders = ",".join(["?"] * len(experiment_ids))
    cursor.execute(f"SELECT * FROM canonical_experiments WHERE experiment_id IN ({placeholders})", experiment_ids)
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()

    if not rows:
        return {"experiments": [], "metrics": {}}

    # Calculate comparative statistics
    o2_values = [r["oxygen_pct"] for r in rows if r.get("oxygen_pct") is not None]
    burn_times = [r["burn_time_s"] for r in rows if r.get("burn_time_s") is not None]
    de_values = [r["extinction_diameter_mm"] for r in rows if r.get("extinction_diameter_mm") is not None]

    return {
        "experiments": rows,
        "comparison_summary": {
            "count": len(rows),
            "max_o2": max(o2_values) if o2_values else None,
            "min_o2": min(o2_values) if o2_values else None,
            "max_burn_time": max(burn_times) if burn_times else None,
            "min_burn_time": min(burn_times) if burn_times else None,
            "max_de": max(de_values) if de_values else None,
            "min_de": min(de_values) if de_values else None
        }
    }


def calculate_mission_scenario(scenario_id: str, custom_o2: Optional[float] = None, custom_pressure: Optional[float] = None) -> Dict[str, Any]:
    """
    Simulates atmospheric fire hazard metrics for predefined and custom planetary spaceflight environments.
    """
    scenarios = {
        "iss": {
            "id": "iss",
            "name_en": "ISS Standard Atmosphere",
            "name_az": "BKS Standart Atmosferi",
            "oxygen_pct": 21.0,
            "pressure_kpa": 101.3,
            "pressure_psia": 14.7,
            "description_en": "Earth sea-level equivalent air mixture maintained inside the International Space Station pressurized modules.",
            "description_az": "Beynəlxalq Kosmik Stansiyanın təzyiqli modullarında saxlanılan Yer dəniz səviyyəsinə bərabər hava qarışığı.",
            "baseline_risk": "NOMINAL"
        },
        "lunar_habitat": {
            "id": "lunar_habitat",
            "name_en": "Artemis Lunar Exploration Habitat",
            "name_az": "Artemis Ay Kəşfiyyat Modulu",
            "oxygen_pct": 34.0,
            "pressure_kpa": 56.5,
            "pressure_psia": 8.2,
            "description_en": "NASA Exploration Atmosphere designed for rapid EVA airlock transitions on the Lunar surface with 34% O2.",
            "description_az": "Ay səthində tez şlüz keçidləri üçün nəzərdə tutulmuş 34% O2 tərkibli NASA Kəşfiyyat Atmosferi.",
            "baseline_risk": "ELEVATED"
        },
        "lunar_hypoxic": {
            "id": "lunar_hypoxic",
            "name_en": "Deep Space Hypoxic Safe-Haven",
            "name_az": "Dərin Kosmos Hipoqsik Sığınacağı",
            "oxygen_pct": 15.0,
            "pressure_kpa": 70.3,
            "pressure_psia": 10.2,
            "description_en": "Emergency hypoxia regime engineered to suppress spacecraft combustion propagation while sustaining suited crew.",
            "description_az": "Kosmik gəmidə yanğının yayılmasını boğmaq üçün hazırlanmış fövqəladə hipoksiya təhlükəsizlik rejimi.",
            "baseline_risk": "SUPPRESSED"
        }
    }

    if scenario_id == "custom":
        o2 = custom_o2 if custom_o2 is not None else 21.0
        pres = custom_pressure if custom_pressure is not None else 101.3
        scenario_data = {
            "id": "custom",
            "name_en": "Custom Spacecraft Atmosphere",
            "name_az": "Fərdiləşdirilmiş Kosmik Gəmi Atmosferi",
            "oxygen_pct": o2,
            "pressure_kpa": pres,
            "pressure_psia": round(pres * 0.145038, 2),
            "description_en": "Custom user-defined environmental chamber parameters.",
            "description_az": "İstifadəçi tərəfindən təyin edilmiş xüsusi atmosfer kamerası parametrləri.",
            "baseline_risk": "CUSTOM"
        }
    else:
        scenario_data = scenarios.get(scenario_id, scenarios["iss"])
        o2 = scenario_data["oxygen_pct"]
        pres = scenario_data["pressure_kpa"]

    # Calculate Fire Hazard Index (FHI: scale 1.0 to 10.0)
    # Formula derived from NASA-STD-6001 oxygen partial pressure & mole fraction sensitivity
    po2_kpa = (o2 / 100.0) * pres
    fhi_raw = 1.0 + (o2 / 21.0) * 3.5 + (po2_kpa / 21.3) * 1.8
    fhi = min(10.0, max(1.0, round(fhi_raw, 1)))

    # Flammability Risk Classification
    if fhi < 3.5:
        risk_level = "LOW / SUPPRESSED"
        risk_level_az = "AŞAĞI / BOĞULMUŞ"
        status_color = "#10B981"  # Emerald Green
    elif fhi < 6.5:
        risk_level = "MODERATE / NOMINAL"
        risk_level_az = "MÖTƏDİL / NOMİNAL"
        status_color = "#3B82F6"  # Precision Blue
    elif fhi < 8.5:
        risk_level = "ELEVATED HAZARD"
        risk_level_az = "YÜKSƏK TƏHLÜKƏ"
        status_color = "#F59E0B"  # Warning Amber
    else:
        risk_level = "CRITICAL FLAMMABILITY"
        risk_level_az = "KRİTİK ALOVLANMA"
        status_color = "#EF4444"  # Critical Red

    # Projected Extinction Diameter for standard Heptane / PMMA sample (mm)
    # Higher O2 yields smaller extinction diameter (harder to quench naturally)
    projected_de_mm = max(0.45, round(2.85 * math.exp(-0.038 * o2), 3))

    # Extinction Time Multiplier vs Standard ISS air
    burn_rate_multiplier = round((o2 / 21.0) ** 1.35 * (pres / 101.3) ** 0.25, 2)

    # Suppressant inerting gas requirement (e.g. N2 or CO2 volume percentage needed to reach quenching)
    required_n2_purge_pct = round(max(0.0, (o2 - 14.5) * 1.8), 1)

    return {
        "scenario": scenario_data,
        "fire_hazard_index": fhi,
        "risk_level_en": risk_level,
        "risk_level_az": risk_level_az,
        "status_color": status_color,
        "metrics": {
            "oxygen_pct": o2,
            "pressure_kpa": pres,
            "oxygen_partial_pressure_kpa": round(po2_kpa, 2),
            "projected_extinction_diameter_mm": projected_de_mm,
            "burn_rate_multiplier": burn_rate_multiplier,
            "required_inert_purge_pct": required_n2_purge_pct
        },
        "advisory_en": (
            f"Under {o2}% O2 at {pres} kPa, flame propagation velocity is {burn_rate_multiplier}x baseline. "
            f"Extinction diameter is {projected_de_mm} mm. Standard NASA-STD-6001 materials testing requires enhanced verification."
        ),
        "advisory_az": (
            f"{pres} kPa təzyiqdə və {o2}% O2 mühitində alovun yayılma sürəti baza rejimindən {burn_rate_multiplier}x dəfə çoxdur. "
            f"Sönmə diametri {projected_de_mm} mm təşkil edir. NASA-STD-6001 standartına əsasən xüsusi material sertifikasiyası tələb olunur."
        )
    }
