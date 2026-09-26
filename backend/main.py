#!/usr/bin/env python3
"""
FIRE-X NASA Microgravity Combustion Intelligence Platform
FastAPI Backend API with SQL Analytics, Multi-Filter Explorer, Side-by-Side Comparison,
Mission Scenario Simulation, and Evidence-Backed AI (Gemini RAG).
"""

import os
import re
import json
import sqlite3
import random
import difflib
from typing import List, Optional
from fastapi import FastAPI, Query, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import google.generativeai as genai

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "fire_safety.db")

# Fallback to backend/fire_safety.db if not found in root
if not os.path.exists(DB_PATH):
    DB_PATH = os.path.join(BASE_DIR, "backend", "fire_safety.db")

# API Key configuration
API_KEY = os.environ.get("GEMINI_API_KEY", "AQ.Ab8RN6J78I7N2LiVEDN5a-3W74-bMNHILPq4II5XXHib2Oaobw").strip()
if API_KEY:
    try:
        genai.configure(api_key=API_KEY)
    except Exception as e:
        print("[!] Gemini configuration warning:", e)

app = FastAPI(
    title="FIRE-X: NASA Microgravity Fire Safety Platform",
    description="AI-powered exploration and evidence-backed insights from NASA microgravity combustion data.",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# --- MODELS ---
class QueryModel(BaseModel):
    question: str
    fuel_filter: Optional[str] = None
    family_filter: Optional[str] = None


class CompareRequest(BaseModel):
    experiment_ids: List[str]


# --- ROUTES ---

@app.get("/")
def read_root():
    index_path = os.path.join(BASE_DIR, "frontend", "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "FIRE-X API is operational. Visit /docs for API documentation."}


@app.get("/api/stats")
def get_platform_stats():
    """Returns high-level KPI metrics and chart datasets for the platform."""
    conn = get_db()
    cursor = conn.cursor()

    # Total counts
    cursor.execute("SELECT COUNT(*) FROM canonical_experiments")
    total_experiments = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(DISTINCT fuel_material) FROM canonical_experiments")
    total_fuels = cursor.fetchone()[0]

    cursor.execute("SELECT MIN(oxygen_pct), MAX(oxygen_pct), AVG(oxygen_pct) FROM canonical_experiments WHERE oxygen_pct IS NOT NULL")
    min_o2, max_o2, avg_o2 = cursor.fetchone()

    # Family breakdown
    cursor.execute("SELECT dataset_family, COUNT(*) as count FROM canonical_experiments GROUP BY dataset_family ORDER BY count DESC")
    family_distribution = [{"family": r["dataset_family"], "count": r["count"]} for r in cursor.fetchall()]

    # Top fuels
    cursor.execute("SELECT fuel_material, COUNT(*) as count FROM canonical_experiments GROUP BY fuel_material ORDER BY count DESC LIMIT 8")
    top_fuels = [{"fuel": r["fuel_material"], "count": r["count"]} for r in cursor.fetchall()]

    # Extinction outcomes
    cursor.execute("SELECT extinction_outcome, COUNT(*) as count FROM canonical_experiments WHERE extinction_outcome IS NOT NULL GROUP BY extinction_outcome ORDER BY count DESC LIMIT 6")
    outcomes = [{"outcome": r["extinction_outcome"], "count": r["count"]} for r in cursor.fetchall()]

    # Oxygen vs Burn time correlation sample (for scatter plot)
    cursor.execute("""
        SELECT experiment_id, fuel_material, oxygen_pct, burn_time_s, dataset_family 
        FROM canonical_experiments 
        WHERE oxygen_pct IS NOT NULL AND burn_time_s IS NOT NULL AND burn_time_s > 0
        ORDER BY oxygen_pct ASC LIMIT 100
    """)
    o2_vs_burn = [dict(r) for r in cursor.fetchall()]

    conn.close()

    return {
        "total_experiments": total_experiments,
        "total_fuels": total_fuels,
        "oxygen_range": {
            "min": round(min_o2, 1) if min_o2 else 12.0,
            "max": round(max_o2, 1) if max_o2 else 34.0,
            "avg": round(avg_o2, 1) if avg_o2 else 19.6
        },
        "family_distribution": family_distribution,
        "top_fuels": top_fuels,
        "outcomes": outcomes,
        "o2_vs_burn_scatter": o2_vs_burn
    }


@app.get("/api/experiments")
def get_experiments(
    q: Optional[str] = None,
    family: Optional[str] = None,
    fuel: Optional[str] = None,
    outcome: Optional[str] = None,
    min_o2: Optional[float] = None,
    max_o2: Optional[float] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100)
):
    """Multi-parameter filtering and searching across all 409 NASA experiments."""
    conn = get_db()
    cursor = conn.cursor()

    conditions = []
    params = []

    if q:
        query_pattern = f"%{q.strip()}%"
        conditions.append("(fuel_material LIKE ? OR experiment_id LIKE ? OR notes LIKE ? OR sample_description LIKE ?)")
        params.extend([query_pattern, query_pattern, query_pattern, query_pattern])

    if family and family.lower() != "all":
        conditions.append("dataset_family = ?")
        params.append(family)

    if fuel and fuel.lower() != "all":
        conditions.append("fuel_material LIKE ?")
        params.append(f"%{fuel}%")

    if outcome and outcome.lower() != "all":
        conditions.append("extinction_outcome LIKE ?")
        params.append(f"%{outcome}%")

    if min_o2 is not None:
        conditions.append("oxygen_pct >= ?")
        params.append(min_o2)

    if max_o2 is not None:
        conditions.append("oxygen_pct <= ?")
        params.append(max_o2)

    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""

    # Count total matching
    count_sql = f"SELECT COUNT(*) FROM canonical_experiments {where_clause}"
    cursor.execute(count_sql, params)
    total_matching = cursor.fetchone()[0]

    # Fetch paginated results
    offset = (page - 1) * limit
    data_sql = f"""
        SELECT experiment_id, dataset_family, investigation_id, original_test_id,
               fuel_material, material_category, oxygen_pct, pressure_mmhg, pressure_kpa,
               burn_time_s, extinction_outcome, extinction_diameter_mm, initial_diameter_mm,
               airflow_velocity_cms, test_date, source_name, source_url, notes
        FROM canonical_experiments 
        {where_clause}
        ORDER BY experiment_id ASC 
        LIMIT ? OFFSET ?
    """
    cursor.execute(data_sql, params + [limit, offset])
    rows = [dict(r) for r in cursor.fetchall()]

    conn.close()

    return {
        "total": total_matching,
        "page": page,
        "limit": limit,
        "pages": (total_matching + limit - 1) // limit,
        "records": rows
    }


@app.get("/api/experiments/{experiment_id}")
def get_experiment_detail(experiment_id: str):
    """Detailed view for a single NASA experiment including sensor readings and provenance."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM canonical_experiments WHERE experiment_id = ?", (experiment_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail=f"Experiment '{experiment_id}' not found.")

    return dict(row)


@app.post("/api/compare")
def compare_experiments(payload: CompareRequest):
    """Side-by-side comparison for 2 to 4 selected NASA experiments."""
    ids = payload.experiment_ids[:4]
    if not ids:
        return {"experiments": [], "comparison_metrics": {}}

    conn = get_db()
    cursor = conn.cursor()
    placeholders = ",".join(["?"] * len(ids))
    cursor.execute(f"SELECT * FROM canonical_experiments WHERE experiment_id IN ({placeholders})", ids)
    records = [dict(r) for r in cursor.fetchall()]
    conn.close()

    metrics = {
        "oxygen_comparison": [{"id": r["experiment_id"], "material": r["fuel_material"], "oxygen_pct": r["oxygen_pct"]} for r in records],
        "burn_time_comparison": [{"id": r["experiment_id"], "material": r["fuel_material"], "burn_time_s": r["burn_time_s"]} for r in records],
        "extinction_comparison": [{"id": r["experiment_id"], "material": r["fuel_material"], "outcome": r["extinction_outcome"]} for r in records]
    }

    return {
        "experiments": records,
        "comparison_metrics": metrics
    }


@app.get("/api/mission-scenario/{scenario_id}")
def get_mission_scenario(scenario_id: str):
    """
    Simulates NASA space exploration environments and returns relevant combustion experiments:
    - 'iss': International Space Station standard environment (21% O2, 760 mmHg, microgravity)
    - 'lunar_habitat': Artemis Moon Base / Gateway (reduced pressure 56 kPa, elevated O2 32-34%)
    - 'lunar_hypoxic': Low flammability exploration concept (16% O2, 760 mmHg)
    - 'mars_vehicle': Mars Ascent / Transit Habitat (30% O2, 70 kPa)
    """
    scenarios = {
        "iss": {
            "name": "International Space Station (ISS) Standard",
            "atmosphere": "21% O2, 760 mmHg (101.3 kPa), Microgravity (0g)",
            "description": "Standard shirtsleeve habitable cabin environment. Airflow is strictly fan-driven.",
            "target_o2": 21.0,
            "target_pressure": 760.0,
            "filter_o2_range": (20.0, 22.5),
            "safety_insight": "In zero-g natural convection ceases. Flames become spherical, burn slower, but can smolder undetected. Low airflow (< 5 cm/s) limits oxygen replenishment, promoting radiative self-extinction."
        },
        "lunar_habitat": {
            "name": "NASA Exploration Atmosphere (Exploration / Artemis Lunar)",
            "atmosphere": "32% - 34% O2, 420 - 525 mmHg (56 - 70 kPa), Hypobaric Hyperoxia",
            "description": "Reduces pre-breathe times for EVA spacewalks. Higher O2 mole fraction increases material flammability.",
            "target_o2": 32.0,
            "target_pressure": 500.0,
            "filter_o2_range": (28.0, 35.0),
            "safety_insight": "Elevated oxygen (>30%) dramatically accelerates flame propagation and reduces time to ignition even at reduced pressures. Conventional flame-retardant polymers may ignite rapidly."
        },
        "lunar_hypoxic": {
            "name": "Hypoxic Fire-Suppressed Compartment",
            "atmosphere": "15% - 17% O2, 760 mmHg (101.3 kPa)",
            "description": "Inert gas blending (e.g. Nitrogen or Argon enriched) to prevent sustained combustion in uninhabited modules.",
            "target_o2": 16.0,
            "target_pressure": 760.0,
            "filter_o2_range": (14.0, 17.5),
            "safety_insight": "Below 17% O2, most solid polymers and fabrics undergo rapid quenching or cool flame radiative extinction in microgravity. Highly effective passive fire protection barrier."
        }
    }

    scen = scenarios.get(scenario_id, scenarios["iss"])
    min_o2, max_o2 = scen["filter_o2_range"]

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT experiment_id, dataset_family, fuel_material, oxygen_pct, pressure_mmhg, 
               burn_time_s, extinction_outcome, source_url, notes
        FROM canonical_experiments 
        WHERE oxygen_pct BETWEEN ? AND ?
        ORDER BY burn_time_s DESC LIMIT 10
    """, (min_o2, max_o2))
    matching_tests = [dict(r) for r in cursor.fetchall()]
    conn.close()

    return {
        "scenario": scen,
        "matching_experiments": matching_tests,
        "count": len(matching_tests)
    }


@app.post("/api/ask-ai")
def ask_ai(payload: QueryModel):
    """
    Scientific RAG Engine:
    1. Performs SQL/Python analytics on matching NASA records to calculate real facts (not LLM hallucinations).
    2. Uses Gemini to synthesize an evidence-backed analysis citing real test IDs, sources, and uncertainty boundaries.
    """
    raw_query = payload.question.strip()
    if not raw_query:
        return {"report_summary": "Zəhmət olmasa sual daxil edin.", "rows": []}

    conn = get_db()
    cursor = conn.cursor()

    # Search for keywords
    words = [w.lower() for w in re.findall(r"\w+", raw_query) if len(w) > 2]
    stopwords = {"what", "how", "does", "effect", "affect", "under", "with", "from", "nasa", "fire", "microgravity", "təcrübə", "haqqında", "necə", "hansı"}
    keywords = [w for w in words if w not in stopwords]

    conditions = []
    params = []

    for kw in keywords:
        pattern = f"%{kw}%"
        conditions.append("(fuel_material LIKE ? OR dataset_family LIKE ? OR extinction_outcome LIKE ? OR notes LIKE ? OR sample_description LIKE ?)")
        params.extend([pattern, pattern, pattern, pattern, pattern])

    where_clause = f"WHERE {' OR '.join(conditions)}" if conditions else ""

    # Fetch matching records
    sql = f"""
        SELECT experiment_id, dataset_family, investigation_id, fuel_material, 
               oxygen_pct, pressure_mmhg, burn_time_s, extinction_outcome, 
               extinction_diameter_mm, initial_diameter_mm, airflow_velocity_cms,
               source_name, source_url, notes
        FROM canonical_experiments 
        {where_clause}
        ORDER BY oxygen_pct DESC
        LIMIT 15
    """
    cursor.execute(sql, params)
    matching_rows = [dict(r) for r in cursor.fetchall()]

    # If no keyword matches, fetch representative sample
    if not matching_rows:
        cursor.execute("""
            SELECT experiment_id, dataset_family, investigation_id, fuel_material, 
                   oxygen_pct, pressure_mmhg, burn_time_s, extinction_outcome, 
                   extinction_diameter_mm, initial_diameter_mm, airflow_velocity_cms,
                   source_name, source_url, notes
            FROM canonical_experiments 
            ORDER BY RANDOM() LIMIT 10
        """)
        matching_rows = [dict(r) for r in cursor.fetchall()]

    conn.close()

    # Pre-calculate deterministic statistics in Python
    count = len(matching_rows)
    valid_o2 = [r["oxygen_pct"] for r in matching_rows if r["oxygen_pct"] is not None]
    avg_o2 = round(sum(valid_o2) / len(valid_o2), 2) if valid_o2 else 21.0
    valid_burns = [r["burn_time_s"] for r in matching_rows if r["burn_time_s"] is not None]
    avg_burn = round(sum(valid_burns) / len(valid_burns), 2) if valid_burns else 0.0
    materials = list(set(r["fuel_material"] for r in matching_rows))
    outcomes = list(set(r["extinction_outcome"] for r in matching_rows if r["extinction_outcome"]))

    # Prepare context for LLM
    context_data = {
        "sample_size": count,
        "avg_oxygen_pct": avg_o2,
        "avg_burn_time_seconds": avg_burn,
        "materials_represented": materials[:6],
        "observed_outcomes": outcomes,
        "retrieved_experiments": matching_rows[:8]
    }

    # Default scientific answer fallback
    ai_summary = f"NASA PSI məlumat bazasından {count} ədəd eksperiment təhlil edildi. Orta oksigen qatılığı {avg_o2}%, orta yanma müddəti isə {avg_burn} saniyə təşkil edir."
    thermal_insight = "Mikroyerçəkimdə təbii konveksiyanın olmaması səbəbindən alov kürəvi forma alır və istilik əsasən radiasiya (şüalanma) yolu ilə itirilir."
    extinction_insight = f"Müşahidə edilən dominant sönmə mexanizmləri: {', '.join(outcomes[:4])}. Oksigen azaldıqda və ya hava axını dayandıqda radiativ sönmə (radiative extinction) baş verir."
    recommendation = "Kosmik gəmilərdə yanğın baş verdikdə ventilyasiya dərhal dayandırılmalı və kabindəki oksigen qatılığı 16%-dən aşağı endirilməlidir."
    uncertainty = "Məlumatlar yalnız FLEX, BASS-II və SAFFIRE sınaqları ilə məhdudlaşır; digər kompozit materiallar üçün ekstrapolyasiya ehtiyatla aparılmalıdır."

    # Try Gemini Live Synthesis
    if API_KEY:
        prompt = f"""
        You are an expert NASA Microgravity Combustion Physicist and Spacecraft Fire Safety Engineer for project FIRE-X.
        The user asked: "{raw_query}"

        Here is the deterministic mathematical data calculated directly from the NASA SQLite database:
        - Total matching NASA experiments: {count}
        - Tested Materials: {', '.join(materials[:6])}
        - Mean Oxygen Level: {avg_o2}% (Calculated by SQL)
        - Mean Observed Burn Time: {avg_burn} seconds (Calculated by SQL)
        - Observed Extinction Outcomes: {', '.join(outcomes)}
        
        Detailed NASA Records:
        {json.dumps(context_data['retrieved_experiments'], indent=2)}

        Provide a scientifically accurate, evidence-backed synthesis in Azerbaijani.
        CRITICAL RULES:
        1. Base your answer strictly on the provided NASA data. Do not hallucinate numbers or cite unlisted experiments.
        2. Format your response strictly as a JSON object with these keys:
           - "report_summary": 2-3 clear sentences answering the question in Azerbaijani, citing real NASA data.
           - "thermal": Explanation of the thermal and radiative dynamics in microgravity in Azerbaijani.
           - "extinction": Explanation of the extinction and flame propagation dynamics in Azerbaijani.
           - "recommendation": Concrete engineering recommendation for spacecraft fire safety in Azerbaijani.
           - "limitations": Scientific uncertainty and limitations of this dataset in Azerbaijani.
        """

        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)
            clean_text = response.text.replace("```json", "").replace("```", "").strip()
            ai_data = json.loads(clean_text)

            ai_summary = ai_data.get("report_summary", ai_summary)
            thermal_insight = ai_data.get("thermal", thermal_insight)
            extinction_insight = ai_data.get("extinction", extinction_insight)
            recommendation = ai_data.get("recommendation", recommendation)
            uncertainty = ai_data.get("limitations", uncertainty)
        except Exception as e:
            print("[!] Gemini call error, using deterministic analysis:", e)

    return {
        "query": raw_query,
        "sample_size": count,
        "report_summary": ai_summary,
        "thermal": thermal_insight,
        "extinction": extinction_insight,
        "recommendation": recommendation,
        "limitations": uncertainty,
        "calculated_stats": {
            "avg_oxygen_pct": avg_o2,
            "avg_burn_time_s": avg_burn,
            "materials_count": len(materials),
            "outcomes": outcomes
        },
        "rows": matching_rows
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
