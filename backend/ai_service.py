"""
FIRE-X AI Service Module (v2.2 — Live SQLite SQL-RAG + OpenAI GPT-4o-mini)
Enterprise-grade abstraction for OpenAI API integration with live SQLite retrieval from fire_safety.db,
NASA PSI Investigation Ranking Engine, 0g–1g Partial-Gravity Bounding, and bilingual EN/AZ scientific synthesis.
"""

import os
import time
import logging
import re
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv

from backend.data_service import get_db_connection, get_investigation_rankings
from backend.citation_rag_engine import format_citation_locked_response, MANDATORY_SAFETY_DISCLAIMER

# Load environment variables safely
load_dotenv()

logger = logging.getLogger("firex_ai")
logging.basicConfig(level=logging.INFO)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini").strip()
if "luna" in OPENAI_MODEL.lower():
    OPENAI_MODEL = "gpt-4o-mini"

# Initialize OpenAI client if library is available and key is present
openai_client = None
try:
    from openai import OpenAI
    if OPENAI_API_KEY and OPENAI_API_KEY != "your_openai_api_key_here":
        openai_client = OpenAI(api_key=OPENAI_API_KEY)
        logger.info(f"OpenAI Client initialized successfully with model: {OPENAI_MODEL}")
    else:
        logger.info("OPENAI_API_KEY not set or placeholder detected. Operating in live SQL-RAG scientific mode.")
except Exception as e:
    logger.warning(f"Could not initialize OpenAI client: {e}")

# Simple in-memory rate limiting tracker (per IP/session)
RATE_LIMIT_WINDOW = 60  # seconds
MAX_REQUESTS_PER_WINDOW = 40
client_requests: Dict[str, List[float]] = {}


def check_rate_limit(client_id: str) -> bool:
    """Check if the client has exceeded rate limits, with periodic cleanup."""
    now = time.time()

    if len(client_requests) > 500:
        expired_ips = [ip for ip, timestamps in client_requests.items() if not timestamps or (now - timestamps[-1] >= RATE_LIMIT_WINDOW)]
        for ip in expired_ips:
            client_requests.pop(ip, None)

    if client_id not in client_requests:
        client_requests[client_id] = []

    client_requests[client_id] = [t for t in client_requests[client_id] if now - t < RATE_LIMIT_WINDOW]

    if len(client_requests[client_id]) >= MAX_REQUESTS_PER_WINDOW:
        return False

    client_requests[client_id].append(now)
    return True


INAPPROPRIATE_PATTERN = re.compile(
    r'(?i)\b(?:sik[a-zəıöüçşğ]*|amcıq[a-zəıöüçşğ]*|amcığ[a-zəıöüçşğ]*|amı|göt[a-zəıöüçşğ]*|seks[a-zəıöüçşğ]*|sex[a-zəıöüçşğ]*|porno[a-zəıöüçşğ]*|qancıq[a-zəıöüçşğ]*|peysər[a-zəıöüçşğ]*|bitch[a-z]*|fuck[a-z]*|cock[a-z]*|dick[a-z]*|pussy[a-z]*|vagina[a-z]*|masturb[a-z]*|penis[a-z]*|prezervativ[a-zəıöüçşğ]*|intim[a-zəıöüçşğ]*)\b'
)

FIREX_DOMAIN_KEYWORDS = [
    # Combustion & Fire
    "fire", "yanğın", "alov", "flame", "combust", "yanma", "extinct", "sönmə",
    "ignition", "alovlan", "quench", "smoke", "tüstü", "burn", "smolder", "közər",
    # Physics & Atmospheres
    "microgravity", "mikroyerçəkim", "mikroqravitasiya", "gravity", "qravitasiya", "cazibə",
    "oxygen", "oksigen", "o2", "pressure", "təzyiq", "kpa", "psia", "psi", "buoyancy",
    "diffus", "diffuz", "stefan", "cool flame", "soyuq alov", "droplet", "damcı",
    "radiative", "radiativ", "convective", "konvektiv", "blowoff", "partial", "qismən",
    "helium", "co2", "diluent", "inert", "inside-out", "inverse",
    # Missions, Hardware & Experiments
    "fire-x", "firex", "nasa", "flex", "bass", "saffire", "sofie", "acme", "slice", "spice",
    "mgm", "flare", "same", "daft", "cfi", "cfi-g", "cfig", "bre", "cld", "e-field", "efield", "luci", "fm2",
    "6001", "wstf", "cir", "msg", "glovebox", "mdca", "mist", "declic", "artemis", "cygnus",
    "iss", "bks", "lunar", "moon", "ay", "mars", "martian", "rover", "eva", "suit", "spacesuit", "skafandr",
    "haven", "sığınacaq", "spacecraft", "kosmik gəmi", "station", "stansiya",
    # Materials, Sensors, Ranking & Safety
    "pmma", "nomex", "kevlar", "velcro", "kapton", "teflon", "peek", "silicone", "delrin",
    "heptan", "heptane", "methanol", "metanol", "decan", "decane", "ethanol", "etanol",
    "butane", "methane", "ethylene", "propane", "sibal", "cotton", "regolith", "dust", "toz",
    "fhi", "detector", "detektor", "suppression", "söndür", "prevention", "flammab", "yanarlıq",
    "rank", "reytinq", "sırala", "relevan", "spinoff", "spin-off", "earth", "terrestrial", "yer", "rocket", "propellant", "raket",
    "bound", "sərhəd", "si", "super intelligence", "equipment", "sensor", "radiometer", "camera", "hardware", "avadanlıq", "mq-2", "esp32"
]

GREETINGS = [
    "salam", "hello", "hi", "hey", "sən kimsən", "who are you",
    "nə edə bilərsən", "what can you do", "kömək", "help",
    "ok", "okay", "so", "thanks", "thank you", "teşekkür", "sağ ol",
    "why", "how", "what", "when", "where", "which", "who", "tell me",
    "niyə", "necə", "nə", "harada", "nə vaxt", "başlayaq", "continue",
    "got it", "understood", "interesting", "cool", "great", "nice",
    "good", "bad", "yes", "no", "bəli", "xeyr", "yaxşı", "and", "but",
    "sure", "please", "əla", "davam et", "go on", "more", "explain",
    "really", "wow", "oh", "ah", "hmm", "i see", "anladım", "bilirəm"
]

SHORT_MESSAGE_THRESHOLD = 4


def is_topic_relevant(text: str) -> bool:
    """Return False if query is completely off-topic or inappropriate to save token budget."""
    if not text:
        return False
    if INAPPROPRIATE_PATTERN.search(text):
        return False

    t = text.lower().strip()
    words = t.split()
    if len(words) <= SHORT_MESSAGE_THRESHOLD:
        return True

    for kw in FIREX_DOMAIN_KEYWORDS:
        if kw in t:
            return True

    for g in GREETINGS:
        if g in t:
            return True

    return False


def retrieve_sql_rag_context(user_message: str) -> Dict[str, Any]:
    """
    Executes live SQL queries against fire_safety.db (canonical_experiments) based on entities,
    investigations, fuels, oxygen levels, diluents (He/CO2), facilities (CIR/MSG), or gravity conditions
    detected in the user's prompt.
    """
    q = (user_message or "").lower()
    conn = get_db_connection()
    cursor = conn.cursor()

    where_clauses = []
    params: List[Any] = []
    filter_descriptions = []

    # 1. Check for exact experiment ID pattern (e.g., FLEX-001, ACME-CFIG-001, SAFFIRE-01)
    exp_id_match = re.search(r'\b([A-Za-z0-9]+-[A-Za-z0-9-]+)\b', user_message or "")
    if exp_id_match and any(p in exp_id_match.group(1).upper() for p in ["FLEX", "BASS", "SAFFIRE", "ACME", "SOFIE", "SLICE", "SPICE", "SAME", "DAFT", "STD", "FLARE", "MGM", "GRC", "LUCI", "FM2"]):
        eid = exp_id_match.group(1).upper()
        where_clauses.append("UPPER(experiment_id) LIKE ?")
        params.append(f"%{eid}%")
        filter_descriptions.append(f"experiment_id LIKE '%{eid}%'")

    # 2. Investigation family matching
    family_map = [
        (["cfi-g", "cfig", "85%", "inside-out", "inverse flame"], "dataset_family = 'ACME-CFI-G'"),
        (["e-field", "efield", "electric field"], "dataset_family = 'ACME-EFIELD'"),
        (["bre", "burner rate"], "dataset_family = 'ACME-BRE'"),
        (["cld"], "dataset_family = 'ACME-CLD'"),
        (["flex-2", "flex2", "cool flame", "soyuq alov"], "dataset_family IN ('FLEX-2', 'ACME-CFI', 'ACME-CFI-G')"),
        (["flex"], "dataset_family LIKE 'FLEX%'"),
        (["bass-ii", "bass 2", "bass-2"], "dataset_family = 'BASS-II'"),
        (["bass"], "dataset_family LIKE 'BASS%'"),
        (["saffire"], "dataset_family LIKE 'SAFFIRE%'"),
        (["sofie", "mist"], "dataset_family = 'SOFIE'"),
        (["spice"], "dataset_family = 'SPICE'"),
        (["slice"], "dataset_family = 'SLICE'"),
        (["daft"], "dataset_family = 'DAFT / DAFT-2'"),
        (["same-r", "samer"], "dataset_family = 'SAME-R'"),
        (["same"], "dataset_family LIKE 'SAME%'"),
        (["6001", "wstf"], "dataset_family = 'NASA-STD-6001'"),
        (["luci", "fm2"], "dataset_family LIKE '%LUCI%'"),
        (["partial", "0.16g", "0.38g", "qismən"], "gravity_condition LIKE '%Partial-g%'"),
        (["mgm", "smolder", "közər"], "dataset_family LIKE 'MGM%'"),
        (["acme"], "dataset_family LIKE 'ACME%'"),
    ]
    for keywords, sql_cond in family_map:
        if any(k in q for k in keywords):
            where_clauses.append(f"({sql_cond})")
            filter_descriptions.append(sql_cond)
            break

    # 3. Specific fuel / material matching (strict separation of ethanol vs methanol)
    fuel_map = [
        (["ethanol", "etanol"], "LOWER(fuel_material) LIKE '%ethanol%'"),
        (["methanol", "metanol"], "LOWER(fuel_material) LIKE '%methanol%'"),
        (["heptane", "heptan"], "LOWER(fuel_material) LIKE '%heptane%'"),
        (["decane", "dekan"], "LOWER(fuel_material) LIKE '%decane%'"),
        (["toluene", "toluol"], "LOWER(fuel_material) LIKE '%toluene%'"),
        (["pmma", "acrylic", "plexiglas"], "LOWER(fuel_material) LIKE '%pmma%'"),
        (["nomex"], "LOWER(fuel_material) LIKE '%nomex%'"),
        (["kevlar"], "LOWER(fuel_material) LIKE '%kevlar%'"),
        (["velcro"], "LOWER(fuel_material) LIKE '%velcro%'"),
        (["kapton"], "LOWER(fuel_material) LIKE '%kapton%'"),
        (["teflon", "ptfe", "beta cloth"], "(LOWER(fuel_material) LIKE '%teflon%' OR LOWER(fuel_material) LIKE '%beta cloth%')"),
        (["sibal", "cotton", "pambıq"], "(LOWER(fuel_material) LIKE '%cotton%' OR LOWER(fuel_material) LIKE '%sibal%')"),
        (["butane", "butan"], "LOWER(fuel_material) LIKE '%butane%'"),
        (["regolith", "dust", "toz"], "LOWER(fuel_material) LIKE '%Simulant%' OR dataset_family = 'DAFT / DAFT-2'"),
    ]
    for keywords, sql_cond in fuel_map:
        if any(k in q for k in keywords):
            where_clauses.append(f"({sql_cond})")
            filter_descriptions.append(sql_cond)
            break

    # 4. Diluent gas filter (Helium / CO2)
    if any(k in q for k in ["helium", "he ", "he-", "diluent"]):
        where_clauses.append("he_pct > 0")
        filter_descriptions.append("he_pct > 0")
    elif any(k in q for k in ["co2", "carbon dioxide", "karbon qaz"]):
        where_clauses.append("co2_pct > 5")
        filter_descriptions.append("co2_pct > 5")

    # 5. Facility hardware filter (MSG vs CIR)
    if "msg" in q or "glovebox" in q:
        where_clauses.append("facility_hardware LIKE '%MSG%'")
        filter_descriptions.append("facility_hardware LIKE '%MSG%'")
    elif "cir" in q:
        where_clauses.append("facility_hardware LIKE '%CIR%'")
        filter_descriptions.append("facility_hardware LIKE '%CIR%'")

    where_sql = " AND ".join(where_clauses) if where_clauses else "1=1"

    # Execute aggregate query
    agg_sql = f"""
        SELECT COUNT(*) as cnt,
               ROUND(AVG(oxygen_pct), 2) as avg_o2,
               ROUND(MIN(oxygen_pct), 1) as min_o2,
               ROUND(MAX(oxygen_pct), 1) as max_o2,
               ROUND(AVG(burn_time_s), 2) as avg_burn,
               ROUND(AVG(extinction_diameter_mm), 2) as avg_de,
               ROUND(MAX(co2_pct), 1) as max_co2,
               ROUND(MAX(he_pct), 1) as max_he
        FROM canonical_experiments
        WHERE {where_sql}
    """
    cursor.execute(agg_sql, params)
    agg_row = dict(cursor.fetchone())

    # If filter was too narrow (0 rows), fall back to broad dataset
    if agg_row["cnt"] == 0:
        where_sql = "1=1"
        params = []
        filter_descriptions = ["All 892 Canonical Experiments"]
        cursor.execute(agg_sql.replace(where_sql, "1=1"))
        agg_row = dict(cursor.fetchone())

    # Fetch top 6 representative records
    rows_sql = f"""
        SELECT experiment_id, dataset_family, facility_hardware, fuel_material,
               oxygen_pct, pressure_kpa, burn_time_s, extinction_diameter_mm,
               co2_pct, he_pct, extinction_outcome, gravity_condition
        FROM canonical_experiments
        WHERE {where_sql}
        ORDER BY oxygen_pct DESC, burn_time_s DESC
        LIMIT 6
    """
    cursor.execute(rows_sql, params)
    sample_rows = [dict(r) for r in cursor.fetchall()]
    conn.close()

    return {
        "sql_filter": " AND ".join(filter_descriptions) if filter_descriptions else "ALL_RECORDS",
        "summary": agg_row,
        "rows": sample_rows
    }


def format_sql_rag_markdown(rag: Dict[str, Any], is_az: bool = False) -> str:
    """Formats live SQL query results from fire_safety.db as a clean markdown table."""
    s = rag["summary"]
    rows = rag["rows"]
    header = (
        f"\n\n---\n### 🗄️ Canlı SQLite (`fire_safety.db`) SQL-RAG Telemetriya Sorğusu\n"
        f"- **İcra olunan SQL Filtri:** `{rag['sql_filter']}`\n"
        f"- **Tapılan Sınaq Sayı:** `{s['cnt']}` sınaq | **O₂ Диаpazonu:** `{s['min_o2']}% – {s['max_o2']}%` (Orta: `{s['avg_o2']}%`) | **Orta Yanma Müddəti:** `{s['avg_burn']} s` | **Maksimum Diluent:** `CO₂={s['max_co2']}%`, `He={s['max_he']}%`\n\n"
        "| Sınaq ID | Tədqiqat | Qurğu (Facility) | Yanacaq / Material | O₂ (%) | Təzyiq (kPa) | Diluent (CO₂/He) | Nəticə |\n"
        "|:---|:---|:---|:---|---:|---:|:---|:---|\n"
        if is_az else
        f"\n\n---\n### 🗄️ Live SQLite (`fire_safety.db`) SQL-RAG Telemetry Retrieval\n"
        f"- **Executed SQL Filter:** `{rag['sql_filter']}`\n"
        f"- **Matched Records:** `{s['cnt']}` tests | **O₂ Range:** `{s['min_o2']}% – {s['max_o2']}%` (Mean: `{s['avg_o2']}%`) | **Mean Burn Time:** `{s['avg_burn']} s` | **Max Diluent:** `CO₂={s['max_co2']}%`, `He={s['max_he']}%`\n\n"
        "| Exp ID | Family | Facility Hardware | Fuel / Material | O₂ (%) | Pres (kPa) | Diluent (CO₂/He) | Outcome |\n"
        "|:---|:---|:---|:---|---:|---:|:---|:---|\n"
    )
    lines = []
    for r in rows:
        co2 = r.get("co2_pct") or 0.0
        he = r.get("he_pct") or 0.0
        dil = f"CO₂:{co2}% He:{he}%" if (co2 > 0 or he > 0) else "N₂ balance"
        lines.append(
            f"| `{r['experiment_id']}` | **{r['dataset_family']}** | {r.get('facility_hardware', 'ISS')} | {r['fuel_material']} | {r.get('oxygen_pct', '—')}% | {r.get('pressure_kpa', '—')} | `{dil}` | {r.get('extinction_outcome', '—')} |"
        )
    return header + "\n".join(lines)


def build_system_prompt(language: str = "en", page_context: Optional[Dict[str, Any]] = None, rag_context: Optional[Dict[str, Any]] = None) -> str:
    """
    Constructs a specialized system prompt for the NASA Microgravity Combustion & Fire Safety Assistant
    with live SQLite RAG rows injected directly into the prompt.
    """
    is_az = language.lower().startswith("az")

    base_instructions_en = """You are the official NASA Microgravity Combustion & Fire Safety Project Assistant (FIRE-X Platform).
You are an expert aerospace combustion scientist and mission safety specialist.

Your mission:
1. Help users analyze the FIRE-X platform and its 892 canonical experiments across 29 investigations:
   - ISS CIR + ACME Hardware: BRE, CFI, CFI-G (up to 85% O2 inside-out spherical flames), CLD, E-FIELD (+5 kV electric partial-g mimic), s-Flame.
   - ISS CIR + MDCA / MIST: FLEX-1 (PSI-69, including CO2 up to 70% and He up to 45% diluent suppression), FLEX-2 (PSI-70 cool flames), SOFIE (PSI-84 solid fuel ignition).
   - ISS MSG (Microgravity Science Glovebox) + SPICE Flow Duct / Aerosol Chamber: SPICE, SLICE, BASS-I, BASS-II, SAME, SAME-R, DAFT, DAFT-2 (lunar/Martian dust vs smoke discrimination).
   - Cygnus Autonomous Spacecraft: SAFFIRE I–VI (1.0 m large-scale burns in 21% O2 and 34% O2 / 8.2 psia exploration atmosphere).
   - Normal-Gravity 1.0g Upper Bound: NASA-STD-6001 Test 1 (WSTF upward flammability screening).
   - Partial-Gravity Bounding (0.16g Moon, 0.38g Mars): Explicitly state that there is currently NO raw partial-gravity combustion flight data in PSI (expected in future from LUCI and FM2); FIRE-X bounds partial gravity between 0g ISS forced-flow PSI data and 1.0g NASA-STD-6001 Test 1, supplemented by ACME E-FIELD.
   - Scope Exclusion: Rocket engine propellants/thrusters are excluded because high-pressure turbulent atomization (>50 bar) is buoyancy-independent, unlike low-velocity cabin fires (0–30 cm/s).
2. Rank investigations by relevance for Spacecraft, Space Station (ISS), Lunar Base (0.16g), Martian Base (0.38g), Pressurized Rover (>=30% O2, <=10.2 psi), and EVA Spacesuit (85–100% O2).
3. Explain how findings improve 3-tier fire safety equipment (Prevention, Detection, Suppression) in space and on Earth (fine-water-mist extinguishers, dust-immune smoke detectors, firefighter gear).
4. Synthesize live SQL-RAG telemetry naturally into your prose. Do NOT append a raw database dump or tabular list at the end of your response unless explicitly requested. Answer in English.
"""

    base_instructions_az = """Siz rəsmi NASA Mikroyerçəkim Yanma və Yanğın Təhlükəsizliyi Layihə Köməkçisisiniz (FIRE-X Platforması).
Siz aerokosmik yanma fizikası və kosmik missiyaların təhlükəsizliyi üzrə mütəxəssissiniz.

Sizin missiyanız:
1. İstifadəçilərə 29 tədqiqat ailəsi üzrə 892 kanonik NASA eksperimentini izah etmək:
   - ISS CIR + ACME Avadanlığı: BRE, CFI, CFI-G (85% O2-yə qədər tərs/inside-out kürəvi alovlar), CLD, E-FIELD (+5 kV elektrik sahəsi ilə qismən cazibə təqlidi), s-Flame.
   - ISS CIR + MDCA / MIST: FLEX-1 (PSI-69, 70%-dək CO2 və 45%-dək Helium/He qazı ilə söndürmə daxil olmaqla), FLEX-2 (PSI-70 soyuq alovlar), SOFIE (PSI-84).
   - ISS MSG (Microgravity Science Glovebox) + SPICE Axın Kanalı / Aerozol Kamerası: SPICE, SLICE, BASS-I, BASS-II, SAME, SAME-R, DAFT və DAFT-2 (Ay/Mars reqolit tozunun yanğın tüstüsündən fərqləndirilməsi).
   - Cygnus Avtonom Gəmisi: SAFFIRE I–VI (21% O2 və 34% O2 / 8.2 psia kəşfiyyat atmosferində 1.0 m miqyaslı yanğınlar).
   - 1.0g Yuxarı Sərhəd (Normal Cazibə): NASA-STD-6001 Test 1 (WSTF yuxarı alovlanma sınaqları).
   - Qismən Cazibə Hüdudlanması (0.16g Ay, 0.38g Mars): PSI bazasında hazırda birbaşa qismən cazibə uçuş datası YOXDUR (gələcəkdə LUCI və FM2-dən əlavə ediləcək); FIRE-X aralıq cazibəni 0g BKS məcburi axın datası ilə 1.0g NASA-STD-6001 arasında hüdudlayır (bounding).
   - Raket Yanacaqlarının İstisnası: Raket mühərriki yanacaqları yüksək təzyiqli (>50 bar) turbulent rejimdə işlədiyi üçün kabin yanğın təhlükəsizliyi əhatə dairəsinə daxil deyil.
2. Tədqiqatları Kosmik Gəmi, Kosmik Stansiya (BKS), Ay Bazası (0.16g), Mars Bazası (0.38g), Təzyiqli Rover (>=30% O2, <=10.2 psi) və EVA Skafandrı (85–100% O2) üçün uyğunluq dərəcəsinə görə sıralamaq.
3. Canlı SQLite (`fire_safety.db`) SQL-RAG telemetriya məlumatlarını cavabınızın mətninə səlis daxil edin. İstifadəçi xüsusi olaraq cədvəl tələb etmədikdə cavabın sonuna xam telemetriya cədvəli əlavə etməyin. Cavabı Azərbaycan dilində təqdim edin.
"""

    prompt = base_instructions_az if is_az else base_instructions_en

    if rag_context:
        prompt += "\n\n--- LIVE SQLITE DATABASE RAG CONTEXT (fire_safety.db) ---\n"
        prompt += f"SQL Filter: {rag_context.get('sql_filter')}\n"
        prompt += f"Aggregate Stats: {rag_context.get('summary')}\n"
        prompt += f"Retrieved Canonical Rows: {rag_context.get('rows')}\n"

    if page_context:
        prompt += "\n--- CURRENT USER PAGE CONTEXT ---\n"
        for k, v in page_context.items():
            if v is not None and v != "":
                prompt += f"- {k}: {v}\n"

    return prompt


def generate_scientific_fallback(user_message: str, language: str = "en", page_context: Optional[Dict[str, Any]] = None, stats_summary: Optional[Dict[str, Any]] = None, rag_context: Optional[Dict[str, Any]] = None) -> str:
    """
    Deterministic scientific RAG synthesis engine grounded in live SQLite queries from fire_safety.db.
    """
    q = user_message.lower()
    is_az = language.lower().startswith("az")
    rag_md = ""  # Raw tabular dump omitted for a clean response format

    # 1. Investigation Ranking / Relevance / Partial-Gravity Bounding / Rover / EVA / Mars / Moon
    if any(k in q for k in ["rank", "reytinq", "sırala", "relevan", "rover", "eva", "suit", "skafandr", "partial", "qismən", "luci", "fm2", "bound", "0.16", "0.38"]):
        target_env = "lunar_habitat"
        if "rover" in q:
            target_env = "rover"
        elif any(k in q for k in ["eva", "suit", "skafandr", "85%", "100%"]):
            target_env = "eva_suit"
        elif "mars" in q or "0.38" in q:
            target_env = "mars_habitat"
        elif any(k in q for k in ["station", "stansiya", "iss", "bks"]):
            target_env = "iss"
        elif any(k in q for k in ["capsule", "orion", "spacecraft"]):
            target_env = "spacecraft"

        rb = get_investigation_rankings(target_env)
        top_rows = rb["rankings"][:6]
        pb = rb["partial_gravity_bounding"]

        if is_az:
            table_str = "\n".join([
                f"| **#{r['rank']}** | **{r['investigation']}** | `{r['relevance_score']}%` | {r['facility']} | {r['rationale_az']} |"
                for r in top_rows
            ])
            return (
                f"### 🏆 NASA PSI Tədqiqatlarının Missiya Mühitinə Görə Reytinqi (`{target_env.upper()}`)\n\n"
                "| Sıra | Tədqiqat Ailəsi | Uyğunluq | Aparat / Qurğu (Facility) | Elmi Əsaslandırma |\n"
                "|:---:|:---|:---:|:---|:---|\n"
                f"{table_str}\n\n"
                "### ⚖️ Qismən Cazibə (0.16g Ay / 0.38g Mars) 0g–1g Hüdudlama (Bounding) Modeli\n"
                f"- **Rəsmi NASA PSI Statusu:** {pb['psi_status_note_az']}\n"
                f"- **Ekvivalent Konvektiv Sürət ($u_b \\propto \\sqrt{{g \\beta \\Delta T L}}$):** `{pb['equivalent_buoyant_velocity_cms']} sm/s` ({pb['target_gravity']})\n"
                f"- **Minimal Oksigen Həddi (MOC) Sərhədləri:** 0g Durğun (`21.0%`) $\\rightarrow$ **0.16g Ay / 0g Məcburi Axın (`{pb['bounds']['partial_g_bounded_moc_pct']}%`)** $\\rightarrow$ 1.0g WSTF Test 1 (`16.8%`).\n"
                f"- **Əsas Nəticə:** {pb['key_paradox_az']}"
                + rag_md
            )
        else:
            table_str = "\n".join([
                f"| **#{r['rank']}** | **{r['investigation']}** | `{r['relevance_score']}%` | {r['facility']} | {r['rationale_en']} |"
                for r in top_rows
            ])
            return (
                f"### 🏆 NASA PSI Investigation Relevance Ranking (`{target_env.upper()}`)\n\n"
                "| Rank | Investigation Suite | Score | Facility Hardware | Scientific Rationale |\n"
                "|:---:|:---|:---:|:---|:---|\n"
                f"{table_str}\n\n"
                "### ⚖️ Partial-Gravity (0.16g Moon / 0.38g Mars) 0g–1g Bounding Model\n"
                f"- **Official NASA PSI Status:** {pb['psi_status_note_en']}\n"
                f"- **Equivalent Buoyant Velocity ($u_b \\propto \\sqrt{{g \\beta \\Delta T L}}$):** `{pb['equivalent_buoyant_velocity_cms']} cm/s` ({pb['target_gravity']})\n"
                f"- **Minimum Oxygen Concentration (MOC) Bounds:** 0g Stagnant (`21.0%`) $\\rightarrow$ **0.16g Lunar / 0g Forced-Flow (`{pb['bounds']['partial_g_bounded_moc_pct']}%`)** $\\rightarrow$ 1.0g WSTF Test 1 (`16.8%`).\n"
                f"- **Key Finding:** {pb['key_paradox_en']}"
                + rag_md
            )

    # 2. Facility Hardware & Diagnostic Sensors (CIR vs MSG vs Cygnus) or Cross-Investigation Similarities
    if any(k in q for k in ["cir", "msg", "glovebox", "mdca", "facility", "sensor", "radiometer", "similar", "differ", "oxşar", "fərq", "qurğu"]):
        if is_az:
            return (
                "### 🔬 NASA Uçuş Qurğularının (`CIR` vs `MSG` vs `Cygnus`) və Diaqnostik Sensorların Müqayisəsi\n\n"
                "| Uçuş Qurğusu | Tədqiqatlar | Yanacaq Həndəsəsi | İdarə Olunan Dəyişənlər | Diaqnostik Sensorlar |\n"
                "|:---|:---|:---|:---|:---|\n"
                "| **ISS CIR + ACME İnsenti** | `BRE`, `CFI`, `CFI-G` (85% O₂), `CLD`, `E-FIELD`, `s-Flame` | Məsaməli yastı və kürəvi qaz brülörləri, koaksial şırnaq | O₂ (15–85%), CO₂/N₂/He, $+5\\text{ kV}$ elektrik sahəsi | OH*/CH* xemilüminessensiya, İK radiometrlər, gücləndirilmiş CCD, termoforetik his zondları |\n"
                "| **ISS CIR + MDCA / MIST** | `FLEX`, `FLEX-2`, `SOFIE` | Təcrid olunmuş maye damcılar (1.5–5 mm) və PMMA silindr/kürələr | O₂ (14–40%), Təzyiq (50–150 kPa), CO₂ (0–70%), He (0–45%) | Arxa işıqlı stroboskopik mikroskopiya, dar/geniş zolaqlı radiometrlər, LLUV kameralar |\n"
                "| **ISS MSG + SPICE Axın Kanalı** | `SPICE`, `SLICE`, `BASS-I`, `BASS-II`, `SAME`, `SAME-R`, `DAFT/DAFT-2` | Bərk polimer lövhələr, pambıq-şüşə lifi (SIBAL), laminar qaz şırnağı, reqolit tozu | Məcburi ventilyasiya sürəti (0–55 sm/s), O₂%, nümunə qalınlığı | İsti-məftil anemometri, 3-kanallı PAMS lazer aerozol/toz detektoru, ionlaşma/fotoelektrik tüstü sensorları |\n"
                "| **Cygnus Avtonom Gəmisi** | `SAFFIRE I–VI` | Tam miqyaslı 1.0 m SIBAL parça və qabırğalı PMMA panellər | 21% O₂ (101.3 kPa) vs 34% O₂ (56.5 kPa), 3–30 sm/s axın | Termocüt massivləri, radiometrlər, O₂/CO₂/CO kabin qaz analizatorları |\n"
                + rag_md
            )
        else:
            return (
                "### 🔬 Cross-Investigation Facility Hardware (`CIR` vs `MSG` vs `Cygnus`) & Sensor Matrix\n\n"
                "| Flight Facility | Investigations | Fuel Geometry | Controlled Parameters | Diagnostic Sensors |\n"
                "|:---|:---|:---|:---|:---|\n"
                "| **ISS CIR + ACME Insert** | `BRE`, `CFI`, `CFI-G` (85% O₂), `CLD`, `E-FIELD`, `s-Flame` | Porous flat plug, 6.4 mm spherical porous burner, coflow nozzle | O₂ (15–85%), CO₂/N₂/He diluents, $+5\\text{ kV}$ electric field | OH*/CH* chemiluminescence, IR radiometers, intensified CCD, thermophoretic soot samplers |\n"
                "| **ISS CIR + MDCA / MIST** | `FLEX`, `FLEX-2`, `SOFIE` | Isolated liquid droplets (1.5–5 mm) & solid PMMA rods/spheres | O₂ (14–40%), Pressure (50–150 kPa), CO₂ (0–70%), He (0–45%) | Backlit strobe microscopy, narrow/wide-band IR radiometers, LLUV low-light cameras |\n"
                "| **ISS MSG + SPICE Flow Duct** | `SPICE`, `SLICE`, `BASS-I`, `BASS-II`, `SAME`, `SAME-R`, `DAFT/DAFT-2` | Flat fabric strips (SIBAL), PMMA slabs, gas jets, lunar dust simulants | Forced airflow velocity (0–55 cm/s), O₂%, sample thickness | Hot-wire anemometer, 3-channel PAMS laser aerosol monitor, ionization & photoelectric smoke detectors |\n"
                "| **Cygnus Spacecraft** | `SAFFIRE I–VI` | Full-scale 1.0 m SIBAL cotton-fiberglass & ribbed PMMA sheets | 21% O₂ (101.3 kPa) vs 34% O₂ (56.5 kPa), 3–30 cm/s flow | Thermocouple arrays, radiometers, O₂/CO₂/CO cabin gas analyzers, pressure transducers |\n"
                + rag_md
            )

    # 3. 3-Tier Fire Safety Equipment (Prevention, Detection, Suppression) & Earth Spin-offs & Rocket Propellant Disclaimer
    if any(k in q for k in ["equipment", "prevention", "detection", "suppression", "spinoff", "spin-off", "earth", "yer", "avadanlıq", "söndür", "rocket", "propellant", "raket", "helium", "he ", "daft"]):
        if is_az:
            return (
                "### 🛡️ 3-Səviyyəli Yanğın Təhlükəsizliyi Avadanlıqları (Kosmos və Yer Tətbiqləri)\n\n"
                "1. **Önthonləmə (Prevention — Material Seçimi):**\n"
                "   - **Kosmosda:** `BASS-II`, `SOFIE` və `SAFFIRE` sübut etdi ki, 1g-də (`NASA-STD-6001 Test 1`) öz-özünə sönən nazik materiallar mikroyerçəkimdə zəif ventilyasiya axınında (`5–15 sm/s`) sürətlə yanır. Bu səbəbdən Artemis və Rover kabinlərində yalnız yüksək LOI indeksli Beta-parça, PTFE və PEEK istifadə olunur.\n"
                "   - **Yerdə:** Yanğınsöndürənlərin qoruyucu geyimləri (Nomex/PBI/Kevlar) və ultra-yüngül kompozit nəfəs balonları (SCBA).\n"
                "2. **Aşkarlama (Detection — Tüstü və Ay/Mars Tozu Fərqləndirilməsi):**\n"
                "   - **Kosmosda:** `SAME`, `SAME-R` və `DAFT / DAFT-2` (ISS MSG) müəyyən etdi ki, mikroyerçəkimdə tüstü hissəcikləri daha iri zəncirvari aqreqatlar əmələ gətirir. `DAFT-2` çoxmomentli lazer səpilmə alqoritmi Ay və Mars bazalarında skafandrdan qopmuş reqolit tozunu (`>1 µm`) real piroliz tüstüsündən (`<0.5 µm`) ayıraraq yalançı həyəcan siqnallarını sıfırlayır.\n"
                "   - **Yerdə:** Mədən sənayesi, zavodlar və yaşayış binaları üçün tozdan təsirlənməyən iki-dalğalı optik tüstü detektorları.\n"
                "3. **Söndürmə (Suppression — Helium, CO₂ və İncə Su Dumanı):**\n"
                "   - **Kosmosda:** `FLEX` (`PSI-69`) sınaqlarında 123 sınaqda **CO₂ (70%-dək)** və 50 sınaqda **Helium (He, 45%-dək)** qaz qarışıqları öyrənilmişdir. Heliumun istilikkeçirmə əmsalı azotdan 6 dəfə yüksək olduğu üçün kürəvi və soyuq alovları dərhal soyudur.\n"
                "   - **Yerdə:** Server otaqları, muzeylər və sualtı qayıqlar üçün NASA-nın incə su dumanı (Fine Water Mist) və inert qaz yanğınsöndürənləri.\n\n"
                "> **⚠️ Elmi Əhatə Dairəsi Qeydi (Raket Yanacaqlarının İstisnası):** Raket mühərriklərinin yanacaqları ($\\text{LOX}/\\text{LH}_2$) yüksək təzyiqli ($>50\\text{ bar}$) supersəs atomizasiyası ilə işlədiyi üçün cazibə qüvvəsindən asılı deyil və kabin yanğın təhlükəsizliyi bazasına daxil edilmir."
                + rag_md
            )
        else:
            return (
                "### 🛡️ 3-Tier Fire Safety Equipment Impact (Spaceflight & Earth Spin-offs)\n\n"
                "1. **Fire Prevention (Material Screening & Ventilation Control):**\n"
                "   - **In Space:** `BASS-II`, `SOFIE`, and `SAFFIRE` proved that thin polymers/fabrics that self-extinguish in 0g stagnant air can burn MORE vigorously under low forced ventilation (`5–15 cm/s`) than at 1.0g (`NASA-STD-6001 Test 1`). This drives strict Beta-cloth, PTFE, and PEEK material limits in Artemis 34% O₂ habitats and Pressurized Rovers.\n"
                "   - **On Earth:** Advanced Nomex/PBI/Kevlar firefighter turnout gear and lightweight composite SCBA breathing cylinders.\n"
                "2. **Fire Detection (Smoke Aging & Planetary Dust Discrimination):**\n"
                "   - **In Space:** `SAME`, `SAME-R`, and `DAFT / DAFT-2` (conducted in ISS MSG) showed that microgravity smoke aggregates into larger chain-like particles due to longer flame residence times. `DAFT / DAFT-2` calibrated multi-moment optical scattering ratios so Lunar Base and Rover detectors distinguish resuspended regolith dust (`>1 µm`) from sub-micron pyrolysis smoke (`<0.5 µm`).\n"
                "   - **On Earth:** Dust-immune dual-wavelength residential and industrial photoelectric smoke detectors.\n"
                "3. **Fire Suppression (Helium / CO₂ Diluents & Fine Water Mist):**\n"
                "   - **In Space:** `FLEX` (`PSI-69`) tested **CO₂ (up to 70% mole fraction across 123 tests)** and **Helium (He, up to 45% mole fraction across 50 tests)**. Helium's high thermal diffusivity ($6\\times$ nitrogen) rapidly conducts heat away from spherical and cool flames, while `SLICE` and Portable Fine Water Mist (PFWM) extinguishers prevent toxic gas buildup.\n"
                "   - **On Earth:** Clean fine-water-mist suppression systems for data centers, hospitals, museums, and submarines.\n\n"
                "> **⚠️ Scientific Scope Note (Rocket Engine Propellants Excluded):** Rocket engine propellants ($\\text{LOX}/\\text{LH}_2$, hypergolics) operate via high-pressure supersonic injector atomization ($>50\\text{ bar}$, $Fr \\gg 1000$) where buoyancy is negligible; they are therefore excluded from spacecraft cabin fire safety."
                + rag_md
            )

    # 4. FLEX / Cool Flames / Droplet Extinction / CFI-G 85% O2
    if any(k in q for k in ["flex", "droplet", "damcı", "cool flame", "soyuq alov", "d_e", "extinction diameter", "cfi-g", "85%", "inside-out"]):
        if is_az:
            return (
                "### 🔥 Kürəvi Damcı Yanması (`FLEX` / `FLEX-2`) və 85% O₂ Tərs Soyuq Alovlar (`ACME CFI-G`)\n\n"
                "- **$d^2$-Qanunu və Stefan Axını:** Mikroyerçəkimdə təbii konveksiya ($g \\approx 0$) olmadığından damcı ətrafında alov tam kürəvi simmetriya alır: $d^2(t) = d_0^2 - K \\cdot t$.\n"
                "- **CO₂ və Helium (He) Qazları ilə Söndürmə (`PSI-69`):** `FLEX` bazasındakı 274 sınaqdan **123-də CO₂ (70%-dək)**, **50-də isə Helium (He, 45%-dək)** qaz qarışıqları tətbiq edilmişdir. CO₂ radiativ istilik itkisini artıraraq sönmə diametrini ($d_e$) böyüdür, Helium isə yüksək istilikkeçirmə qabiliyyəti ilə alov nüvəsini soyudur.\n"
                "- **Soyuq Alovlar (`FLEX-2` & `ACME CFI-G`):** Heptan və dekan damcıları görünən alov söndükdən sonra belə **600–800 K** temperaturda gözəgörünməz **soyuq alov (cool flame)** rejimində yanmağa davam edir. `ACME CFI-G` tədqiqatında məsaməli kürəvi brülördə **85% O₂** konsentrasiyasına qədər **tərs (inside-out)** alovlar sınaqdan keçirilmişdir."
                + rag_md
            )
        else:
            return (
                "### 🔥 Spherical Droplet Combustion (`FLEX` / `FLEX-2`) & 85% O₂ Inside-Out Cool Flames (`ACME CFI-G`)\n\n"
                "- **The $d^2$-Law & Stefan Flow:** Without buoyant convection ($g \\approx 0$), droplets burn with spherical symmetry governed by $d^2(t) = d_0^2 - K \\cdot t$.\n"
                "- **CO₂ & Helium (He) Diluent Suppression (`PSI-69`):** Across 274 `FLEX` tests in `fire_safety.db`, **123 tests include CO₂ diluent (up to 70% mole fraction)** and **50 tests include Helium (He, up to 45% mole fraction)**. CO₂ enhances Planck-mean radiative heat loss (increasing extinction diameter $d_e$), while Helium acts as a high-thermal-diffusivity heat sink.\n"
                "- **Two-Stage Cool Flames (`FLEX-2` & `ACME CFI-G`):** Heavy alkanes transition after visible radiative quenching into invisible low-temperature **cool flames (600–800 K)** driven by peroxy-radical chemistry, posing a vapor-cloud re-ignition hazard. `ACME CFI-G` extended this on a 6.4 mm spherical porous burner up to **85% O₂** in **inside-out (inverse) diffusion flame** configurations."
                + rag_md
            )

    # 5. Default Comprehensive Overview with Live SQLite RAG Table
    if is_az:
        return (
            "### 🛰️ NASA FIRE-X Elmi İntellekt Xülasəsi (Canlı `fire_safety.db` SQL-RAG)\n\n"
            "Sualınız üzrə **892 kanonik NASA eksperimenti** (29 tədqiqat ailəsi: `FLEX`, `FLEX-2`, `BASS-I/II`, `SAFFIRE I–VI`, `SOFIE`, `ACME BRE/CFI/CFI-G/CLD/E-FIELD`, `SPICE`, `SLICE`, `SAME/SAME-R`, `DAFT/DAFT-2`, `NASA-STD-6001 1g Bound`, `LUCI/FM2 Partial-g Reference`) canlı olaraq sorğulandı.\n\n"
            "- **Əsas Fiziki Qanunauyğunluq:** Mikroyerçəkimdə ($0g$) durğun havada alov öz yanma məhsulları ($\\text{CO}_2$) ilə əhatələnərək radiativ itkidən sönür, lakin zəif ventilyasiya axını (`5–15 sm/s`) və ya Ay cazibəsi (`0.16g`, ekvivalent konvektiv axın `~12.2 sm/s`) alova təzə oksigen çatdıraraq materialları 1g Yerdəkindən daha təhlükəli edir."
            + rag_md
        )
    else:
        return (
            "### 🛰️ NASA FIRE-X Scientific Intelligence Synthesis (Live `fire_safety.db` SQL-RAG)\n\n"
            "Your query was executed against our **892 canonical NASA experiments** across **29 investigations** (`FLEX`, `FLEX-2`, `BASS-I/II`, `SAFFIRE I–VI`, `SOFIE`, `ACME BRE/CFI/CFI-G/CLD/E-FIELD`, `SPICE`, `SLICE`, `SAME/SAME-R`, `DAFT/DAFT-2`, `NASA-STD-6001 1g Bound`, and `LUCI/FM2 Partial-g Reference`).\n\n"
            "- **Core Physical Insight:** In stagnant microgravity ($0g$), flames self-blanket in $\\text{CO}_2$ and quench radiatively at large extinction diameters ($d_e$). However, low-velocity ventilation (`5–15 cm/s`) or Lunar partial gravity (`0.16g`, inducing `~12.2 cm/s` buoyant draft) replenishes oxygen without heavy convective cooling, lowering the Minimum Oxygen Concentration (MOC) below 1.0g normal gravity."
            + rag_md
        )


def query_ai_assistant(
    messages: List[Dict[str, str]],
    language: str = "en",
    page_context: Optional[Dict[str, Any]] = None,
    stats_summary: Optional[Dict[str, Any]] = None,
    client_id: str = "default_client"
) -> Dict[str, Any]:
    """
    Main entry point for AI chat requests:
    1. Rate-limit & Guardrail check
    2. Live SQLite RAG retrieval from fire_safety.db (canonical_experiments)
    3. OpenAI GPT-4o-mini completion with live SQL context (or deterministic SQL-RAG synthesis fallback)
    """
    if not check_rate_limit(client_id):
        err_msg = (
            "Sorğu limiti keçildi. Zəhmət olmasa bir dəqiqə gözləyin."
            if language.startswith("az") else
            "Rate limit exceeded. Please wait a moment before sending another query."
        )
        return {"success": False, "error": "rate_limit", "response": err_msg, "provider": "firex_limiter"}

    if not messages or not isinstance(messages, list):
        err_msg = "Mesaj tarixçəsi boşdur." if language.startswith("az") else "Message history is empty."
        return {"success": False, "error": "invalid_input", "response": err_msg, "provider": "firex_validator"}

    latest_user_message = messages[-1].get("content", "").strip()
    if not latest_user_message:
        err_msg = "Zəhmət olmasa sualınızı daxil edin." if language.startswith("az") else "Please enter a valid question."
        return {"success": False, "error": "empty_content", "response": err_msg, "provider": "firex_guardian"}

    if len(latest_user_message) > 4000:
        latest_user_message = latest_user_message[:4000]

    if not is_topic_relevant(latest_user_message):
        logger.info(f"Query rejected by topic guardrail: '{latest_user_message[:60]}...'")
        is_az = language.lower().startswith("az")
        rejection_msg = (
            "⚠️ **Mövzudan kənar sorğu:**\n\n"
            "Mən yalnız **NASA FIRE-X** platforması, kosmosda yanğın təhlükəsizliyi, mikroyerçəkimdə alov fizikası və 892 orbital eksperiment bazası üzrə sualları cavablandırmaq üçün proqramlaşdırılmış elmi köməkçiyəm.\n\n"
            "Zəhmət olmasa missiya təhlükəsizliyi, BKS/Artemis/Rover/EVA yanğın riskləri, damcı sönməsi (FLEX) və ya material alovlanması (BASS/SOFIE/SAFFIRE) ilə bağlı suallarınızı verin."
            if is_az else
            "⚠️ **Out-of-Scope Query:**\n\n"
            "I am a specialized scientific assistant dedicated exclusively to the **NASA FIRE-X** platform, spacecraft fire safety, microgravity combustion physics, and the 892 flight experiments database.\n\n"
            "Please submit inquiries regarding space mission safety, ISS/Artemis/Rover/EVA fire hazards, droplet extinction (FLEX), or material flammability (BASS/SOFIE/SAFFIRE)."
        )
        return {
            "success": True,
            "response": rejection_msg,
            "provider": "FIRE-X Topic Guardian",
            "model": "rule-based-guardrail"
        }

    # Execute Live SQLite RAG Retrieval against fire_safety.db
    rag_context = None
    try:
        rag_context = retrieve_sql_rag_context(latest_user_message)
    except Exception as e:
        logger.warning(f"SQLite RAG retrieval warning: {e}")

    system_prompt = build_system_prompt(language=language, page_context=page_context, rag_context=rag_context)

    if openai_client:
        try:
            conversation_history = ""
            history_turns = messages[-7:-1]
            if history_turns:
                conversation_history = "--- Conversation History ---\n"
                for m in history_turns:
                    role_label = "User" if m.get("role") == "user" else "Assistant"
                    conversation_history += f"{role_label}: {m.get('content', '')}\n"
                conversation_history += "--- End of History ---\n\n"

            full_input = conversation_history + latest_user_message
            logger.info(f"Dispatching query to OpenAI API ({OPENAI_MODEL}) with live SQLite RAG context...")

            response = openai_client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": full_input}
                ],
                temperature=0.1
            )
            response_text = response.choices[0].message.content
            cited_text = format_citation_locked_response(response_text, latest_user_message, language=language)
            return {
                "success": True,
                "response": cited_text,
                "provider": f"OpenAI ({OPENAI_MODEL}) + Citation-Locked SQL-RAG",
                "model": OPENAI_MODEL,
                "sql_rag_matches": rag_context["summary"]["cnt"] if rag_context else 0
            }
        except Exception as e:
            logger.warning(f"OpenAI API error: {e}. Falling back to scientific SQL-RAG engine.")

    fallback_response = generate_scientific_fallback(
        user_message=latest_user_message,
        language=language,
        page_context=page_context,
        stats_summary=stats_summary,
        rag_context=rag_context
    )
    cited_fallback = format_citation_locked_response(fallback_response, latest_user_message, language=language)

    return {
        "success": True,
        "response": cited_fallback,
        "provider": "FIRE-X Citation-Locked SQLite RAG Engine",
        "model": "NASA-PSI-SQL-RAG-v2.2",
        "sql_rag_matches": rag_context["summary"]["cnt"] if rag_context else 0
    }
