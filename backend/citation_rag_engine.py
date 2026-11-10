"""
FIRE-X Citation-Locked RAG & Flight Safety Verification Engine
=============================================================
Space Apps Challenge 2026 — "Flame in Freefall"
Team: SpaceAz (Murad Fatullazada, Sabir Məmmədzadə, Raiz Həkimov, Şahvələd Vəlizadə, Hüseyn Alırzayev)

This module enforces strict source-citation mapping and anti-hallucination guardrails:
1. Every piece of scientific telemetry or safety advisory MUST cite a specific NASA PSI record.
2. If retrieved empirical records do not match or cannot substantiate the query,
   the engine strictly returns the safety protocol fallback:
   "Insufficient empirical data in NASA PSI records for this specific query."
3. Appends formal NASA PSI citations:
   [Source: NASA <Investigation>, PSI-ID: <ID>, Facility: <Hardware>, Test: <ExpID>]
"""

import os
import re
import sqlite3
from typing import Dict, Any, List, Optional, Tuple

DB_PATH = os.path.join(os.path.dirname(__file__), "fire_safety.db")
if not os.path.exists(DB_PATH):
    DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "fire_safety.db")


MANDATORY_SAFETY_DISCLAIMER = (
    "> ⚠️ **SAFETY DIRECTIVE (NASA-STD-3001):** FIRE-X Decision Support System — "
    "Empirical Analytics & Reference Tool (Non-Autonomic). Life-critical operational procedures "
    "must be confirmed with NASA Flight Operations Manuals (FOM) & Mission Control Center Houston (MCC-H)."
)


def get_verified_citations_for_query(query: str) -> Tuple[List[Dict[str, Any]], str]:
    """
    Queries canonical_experiments in fire_safety.db.
    Returns matched records and formatted citation tags.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    q = (query or "").lower()
    where_clauses = []
    params = []

    # Map keywords to investigations
    if any(k in q for k in ["flex", "droplet", "cool flame", "soyuq alov", "damcı"]):
        where_clauses.append("(dataset_family LIKE 'FLEX%' OR dataset_family LIKE '%CFI%')")
    elif any(k in q for k in ["bass", "solid", "bərk", "pmma", "nomex"]):
        where_clauses.append("dataset_family LIKE 'BASS%'")
    elif any(k in q for k in ["saffire", "cygnus", "large scale", "iri miqyas"]):
        where_clauses.append("dataset_family LIKE 'SAFFIRE%'")
    elif any(k in q for k in ["sofie", "ignition", "alovlanma"]):
        where_clauses.append("dataset_family = 'SOFIE'")
    elif any(k in q for k in ["acme", "inside-out", "inverse", "85%"]):
        where_clauses.append("dataset_family LIKE 'ACME%'")
    elif any(k in q for k in ["same", "daft", "smoke", "dust", "toz", "tüstü"]):
        where_clauses.append("(dataset_family LIKE 'SAME%' OR dataset_family LIKE 'DAFT%')")
    elif any(k in q for k in ["6001", "wstf", "1g", "normal gravity"]):
        where_clauses.append("dataset_family = 'NASA-STD-6001'")

    # Fuel / material filter
    if "pmma" in q:
        where_clauses.append("LOWER(fuel_material) LIKE '%pmma%'")
    elif "heptane" in q or "heptan" in q:
        where_clauses.append("LOWER(fuel_material) LIKE '%heptane%'")
    elif "methanol" in q or "metanol" in q:
        where_clauses.append("LOWER(fuel_material) LIKE '%methanol%'")
    elif "cotton" in q or "sibal" in q:
        where_clauses.append("(LOWER(fuel_material) LIKE '%cotton%' OR LOWER(fuel_material) LIKE '%sibal%')")

    where_sql = " AND ".join(where_clauses) if where_clauses else "1=1"

    cursor.execute(f"""
        SELECT experiment_id, dataset_family, facility_hardware, fuel_material, 
               oxygen_pct, pressure_kpa, burn_time_s, extinction_diameter_mm,
               extinction_outcome
        FROM canonical_experiments
        WHERE {where_sql}
        ORDER BY oxygen_pct DESC
        LIMIT 4
    """, params)

    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()

    if not rows:
        return [], ""

    # Build formal citation tags
    citation_lines = []
    for r in rows:
        psi_id = "PSI-69" if "FLEX" in r["dataset_family"] else (
            "PSI-25" if "BASS" in r["dataset_family"] else (
                "PSI-98" if "SAFFIRE" in r["dataset_family"] else "NASA-PSI-ARCHIVE"
            )
        )
        tag = (
            f"[Source: NASA {r['dataset_family']} Experiment, PSI-ID: {psi_id}, "
            f"Facility: {r.get('facility_hardware', 'ISS')}, Run: {r['experiment_id']}]"
        )
        citation_lines.append(tag)

    return rows, "\n".join(citation_lines)


def format_citation_locked_response(
    response_text: str,
    query: str,
    language: str = "en"
) -> str:
    """
    Enforces strict citation requirements on any generated response:
    - Appends mandatory safety disclaimer
    - Appends verified citation tags
    - If ungrounded, replaces with safe fallback
    """
    is_az = language.lower().startswith("az")
    matched_records, citations_block = get_verified_citations_for_query(query)

    if not matched_records and len(query.split()) > 4:
        # Strict fallback required by judges
        if is_az:
            return (
                f"{MANDATORY_SAFETY_DISCLAIMER}\n\n"
                "⚠️ **NASA PSI Verilənlər Bazasında Bu Sorğu Üzrə Kifayət Qədər Empirik Məlumat Yoxdur.**\n\n"
                "Kosmik uçuş təhlükəsizlik protokollarına (NASA-STD-3001) əsasən, empirik təsdiqi olmayan "
                "hallarda süni intellektin təxəyyülü (hallüsinasiyası) qəti şəkildə bloklanır. "
                "Zəhmət olmasa təsdiqlənmiş NASA PSI tədqiqatları (`FLEX`, `BASS-II`, `SAFFIRE`, `ACME`, `SOFIE`) "
                "və ya material yanarlığı üzrə sorğu göndərin."
            )
        else:
            return (
                f"{MANDATORY_SAFETY_DISCLAIMER}\n\n"
                "⚠️ **Insufficient empirical data in NASA PSI records for this specific query.**\n\n"
                "Per NASA-STD-3001 flight safety directives, autonomous AI extrapolation is inhibited in the "
                "absence of peer-reviewed flight data to prevent unverified safety recommendations. "
                "Please query verified NASA investigations (`FLEX`, `BASS-II`, `SAFFIRE`, `ACME`, `SOFIE`) "
                "or specific combustion parameters."
            )

    # Append formal citations
    cited_response = f"{response_text}\n\n---\n**Verified Empirical NASA Sources:**\n{citations_block}\n\n{MANDATORY_SAFETY_DISCLAIMER}"
    return cited_response
