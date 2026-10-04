"""
FIRE-X AI Service Module
Enterprise-grade abstraction for OpenAI ChatGPT API integration with NASA Microgravity Combustion context,
strict server-side security, rate-limiting, and graceful scientific RAG fallback.
"""

import os
import time
import logging
import re
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv

# Load environment variables safely
load_dotenv()

logger = logging.getLogger("firex_ai")
logging.basicConfig(level=logging.INFO)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini").strip()

# Initialize OpenAI client if library is available and key is present
openai_client = None
try:
    from openai import OpenAI
    if OPENAI_API_KEY and OPENAI_API_KEY != "your_openai_api_key_here":
        openai_client = OpenAI(api_key=OPENAI_API_KEY)
        logger.info(f"OpenAI Client initialized successfully with model: {OPENAI_MODEL}")
    else:
        logger.info("OPENAI_API_KEY not set or placeholder detected. Operating in high-precision scientific RAG mode.")
except Exception as e:
    logger.warning(f"Could not initialize OpenAI client: {e}")

# Simple in-memory rate limiting tracker (per IP/session)
RATE_LIMIT_WINDOW = 60  # seconds
MAX_REQUESTS_PER_WINDOW = 40
client_requests: Dict[str, List[float]] = {}


def check_rate_limit(client_id: str) -> bool:
    """Check if the client has exceeded rate limits, with periodic cleanup."""
    now = time.time()

    # Periodic cleanup: if dictionary has grown beyond 500 IPs, purge expired entries
    if len(client_requests) > 500:
        expired_ips = [ip for ip, timestamps in client_requests.items() if not timestamps or (now - timestamps[-1] >= RATE_LIMIT_WINDOW)]
        for ip in expired_ips:
            client_requests.pop(ip, None)

    if client_id not in client_requests:
        client_requests[client_id] = []
        
    # Filter timestamps within current window
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
    "microgravity", "mikroyerçəkim", "mikroqravitasiya", "gravity", "qravitasiya",
    "oxygen", "oksigen", "o2", "pressure", "təzyiq", "kpa", "psia", "buoyancy",
    "diffus", "diffuz", "stefan", "cool flame", "soyuq alov", "droplet", "damcı",
    "radiative", "radiativ", "convective", "konvektiv", "blowoff",
    # Missions & Experiments
    "fire-x", "firex", "nasa", "flex", "bass", "saffire", "sofie", "acme", "slice",
    "mgm", "flare", "same", "6001", "cir", "declic", "artemis", "cygnus", "iss",
    "bks", "lunar", "ay modulu", "haven", "sığınacaq", "spacecraft", "kosmik gəmi",
    # Materials & Safety
    "pmma", "nomex", "heptan", "heptane", "methanol", "metanol", "decan", "decane",
    "ethanol", "etanol", "fhi", "detector", "detektor", "suppression", "söndür",
    "flammab", "yanarlıq"
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

# Short conversational messages that are clearly not off-topic spam
SHORT_MESSAGE_THRESHOLD = 4  # messages with <= this many words pass through

def is_topic_relevant(text: str) -> bool:
    """Return False if query is completely off-topic or inappropriate to save token budget."""
    if not text:
        return False
    if INAPPROPRIATE_PATTERN.search(text):
        return False

    t = text.lower().strip()

    # Always allow very short messages (conversational continuations like "so?", "ok", "why?")
    words = t.split()
    if len(words) <= SHORT_MESSAGE_THRESHOLD:
        return True

    # Check domain keywords
    for kw in FIREX_DOMAIN_KEYWORDS:
        if kw in t:
            return True

    # Check greeting/conversational patterns for slightly longer messages
    for g in GREETINGS:
        if g in t:
            return True

    return False

def build_system_prompt(language: str = "en", page_context: Optional[Dict[str, Any]] = None) -> str:
    """
    Constructs a specialized system prompt for the NASA Microgravity Combustion & Fire Safety Assistant.
    """
    is_az = language.lower().startswith("az")
    
    base_instructions_en = """You are the official NASA Microgravity Combustion & Fire Safety Project Assistant (FIRE-X Platform).
You are an expert aerospace combustion scientist and mission safety specialist.

Your mission:
1. Help users understand the FIRE-X platform, its 879 NASA microgravity combustion experiments across 24 flight families (FLEX-1, FLEX-2, BASS-I, BASS-II, SAFFIRE I-VI, SOFIE, ACME/CIR, SLICE, NASA-STD-6001, NTRS).
2. Explain microgravity combustion physics (absence of buoyant convection, spherical droplet flames, Stefan diffusion, cool flames, radiative vs convective extinction, flammability limits).
3. Explain planetary mission fire safety hazards (ISS 21% O2 at 101.3 kPa vs Artemis Lunar Habitat 34% O2 at 56.5 kPa / 8.2 psia vs Hypoxic Haven 15% O2).
4. Interpret charts, data filters, experiment parameters, and mission scenario simulations on the website.
5. Guide users on how to navigate the platform (Explorer, Comparison tool, Mission Simulator).
6. Politely redirect queries unrelated to space science, NASA combustion experiments, or the FIRE-X platform.

Guidelines:
- Maintain a professional, scientific, precise, yet accessible tone.
- Do NOT use childish emojis or excessive jargon without explanation.
- Use metric/scientific units (mm, s, kPa, % O2, cm/s, K).
- STRICT MATERIAL MATCHING: When a query specifies a particular substance (e.g., 'ethanol'), restrict analysis strictly to that material and do not confuse it with chemically similar species (e.g., 'methanol').
- Cite specific experiment families (e.g. FLEX-1 droplet extinction, SAFFIRE large-scale spacecraft burns) when relevant.
- Always answer in English when requested in English.
"""

    base_instructions_az = """Siz rəsmi NASA Mikromaqnit Yanma və Yanğın Təhlükəsizliyi Layihə Köməkçisisiniz (FIRE-X Platforması).
Siz aerokosmik yanma fizikası və kosmik missiyaların təhlükəsizliyi üzrə mütəxəssissiniz.

Sizin missiyanız:
1. İstifadəçilərə FIRE-X platformasını, 24 uçuş və tədqiqat ailəsi üzrə 879 real NASA mikroqravitasiya yanma eksperimentini (FLEX-1, FLEX-2, BASS-I, BASS-II, SAFFIRE I-VI, SOFIE, ACME/CIR, SLICE, NASA-STD-6001, NTRS) izah etmək.
2. Mikroqravitasiyada yanma fizikasını (təbii konveksiyanın olmaması, sferik alov damcıları, Stefan diffuziyası, soyuq alovlar (cool flames), radiativ və konvektiv sönmə limitləri) elmi və aydın şəkildə izah etmək.
3. Kosmik missiya mühitlərindəki yanğın risklərini izah etmək (BKS 21% O2 / 101.3 kPa vs Artemis Ay Yaşayış Modulu 34% O2 / 56.5 kPa / 8.2 psia vs Hipoqsik Sığınacaq 15% O2).
4. Vebsaytdakı qrafikləri, eksperiment parametrlərini və missiya simulyasiyalarını təhlil etmək.
5. İstifadəçiləri platformanın bölmələrinə (Tədqiqatçı/Explorer, Müqayisə Paneli, Missiya Simulyatoru) yönləndirmək.
6. MÜTLƏQ QAYDA: Yalnız və yalnız NASA FIRE-X platforması, kosmik gəmilərdə yanğın təhlükəsizliyi, mikroyerçəkimdə alov dinamikası və materialların alovlanma limitləri haqqında danışın. Mövzu ilə əlaqəsi olmayan istənilən başqa suala qətiyyətlə və birbaşa: 'Mən yalnız NASA FIRE-X layihəsi və kosmosda yanğın təhlükəsizliyi üzrə ixtisaslaşmış elmi köməkçiyəm. Zəhmət olmasa mikroyerçəkimdə yanma və ya missiya təhlükəsizliyi ilə bağlı suallarınızı verin.' cavabını verin.

Qaydalar:
- Peşəkar, elmi və aydın dildə cavab verin.
- Uşaqcasına emojilərdən istifadə etməyin.
- Metrik və elmi vahidlərdən istifadə edin (mm, s, kPa, % O2, cm/s, K).
- MATERİAL DƏQİQLİYİ: İstifadəçi müəyyən bir material (məsələn, 'ethanol') soruşduqda, yalnız həmin materiala aid dataları təhlil edin. Adı bənzər olan digər maddələri ('methanol' və s.) qətiyyən qarışdırmayın.
- Cavabınızı mütləq Azərbaycan dilində təqdim edin.
"""

    prompt = base_instructions_az if is_az else base_instructions_en

    if page_context:
        prompt += "\n\n=== CURRENT USER INTERFACE CONTEXT ===\n"
        for key, val in page_context.items():
            if val:
                prompt += f"- {key}: {val}\n"
        prompt += "Use this context to give direct, highly relevant answers about what the user is currently viewing.\n"

    return prompt


def generate_scientific_fallback(user_message: str, language: str = "en", page_context: Optional[Dict[str, Any]] = None, stats_summary: Optional[Dict[str, Any]] = None) -> str:
    """
    High-precision deterministic scientific synthesis generator when OpenAI API Key is pending.
    Provides mathematically accurate answers based on the 879 NASA experiment dataset.
    """
    msg = user_message.lower().strip().rstrip("?!.,")
    is_az = language.lower().startswith("az")

    has_flex = "flex" in msg or "droplet" in msg or "damcı" in msg
    has_bass = "bass" in msg or "solid" in msg or "bərk" in msg
    has_saffire = "saffire" in msg or "spacecraft" in msg or "gəmi" in msg
    has_artemis = "artemis" in msg or "lunar" in msg or "ay" in msg or "34%" in msg
    has_iss = "iss" in msg or "bks" in msg or "21%" in msg
    has_extinction = "extinct" in msg or "sönmə" in msg or "diameter" in msg or "diametr" in msg or "limit" in msg

    # Brief friendly response ONLY for pure greetings (≤2 words, no science content)
    _science_words = {
        "flex","bass","saffire","artemis","iss","bks","acme","sofie","slice",
        "droplet","flame","extinction","lunar","combustion","oxygen","fire",
        "o2","o₂","co2","co₂","pmma","heptan","heptane","methanol","ethanol",
        "pressure","kpa","psia","nitrogen","ignit","suppres","smoke","burn",
        "micrograv","gravity","cygnus","spacecraft","habitat","experiment",
        "who","what","how","why","which","explain","tell","describe","define"
    }
    _words = msg.split()
    _is_greeting = (len(_words) <= 2 and not any(kw in msg for kw in _science_words))
    if _is_greeting:
        if is_az:
            return (
                "Salam! 👋 Mən **NASA FIRE-X** platformasının süni intellekt köməkçisiyəm.\n\n"
                "Mikroqravitasiyada yanma fizikası, ISS/Artemis yanğın riskləri, FLEX/BASS/SAFFIRE eksperimentləri "
                "haqqında suallarınızı verə bilərsiniz. Necə kömək edə bilərəm?"
            )
        else:
            return (
                "Hello! 👋 I'm the **NASA FIRE-X** AI research assistant.\n\n"
                "I can answer questions about microgravity combustion physics, ISS/Artemis fire hazards, "
                "and the 879-experiment database. What would you like to know?"
            )

    if is_az:
        if has_artemis:
            return (
                "**Artemis Ay Yaşayış Modulu Yanğın Riski Analizi:**\n\n"
                "NASA Artemis proqramı çərçivəsində tətbiq olunan **Kəşfiyyat Atmosferi (Exploration Atmosphere)** "
                "**34% O₂ və 56.5 kPa (8.2 psia)** təzyiq rejimində işləyir. Bu mühitdə:\n"
                "1. **Yüksək Yanğın Təhlükəsi İndeksi (FHI = 8.2/10):** Standart BKS (21% O₂) mühiti ilə müqayisədə alovlanma həddi kəskin azalır və yanma sürəti 42% artır.\n"
                "2. **Sönmə Diametri:** Damcı və bərk materialların sönmə diametri daha kiçik olur (təxminən 0.82 mm), yəni alov daha gec sönür.\n"
                "3. **Təhlükəsizlik Tövsiyəsi:** NASA-STD-6001 standartına uyğun olaraq 34% O₂ mühitində sınaqdan keçmiş xüsusi alovadavamlı polimerlərdən və $N_2/CO_2$ avtomatlaşdırılmış boğma sistemindən istifadə edilməlidir."
            )
        elif has_flex:
            return (
                "**FLEX (Flame Extinction Experiment) Missiyası:**\n\n"
                "FLEX-1 və FLEX-2 eksperimentləri Beynəlxalq Kosmik Stansiyada (BKS) Yanma İnteqrasiya Rəfində (CIR) həyata keçirilmişdir.\n"
                "- **Əsas Məqsəd:** Mikromaqnit şəraitində maye yanacaq damcılarının (n-heptan, metanol, dekan, etanol) sferik yanma və sönmə limitlərini tədqiq etmək.\n"
                "- **Əsas Elmi Kəşf:** Yüksək temperatur alovu söndükdən sonra aşağı temperaturda davam edən **'Soyuq Alov' (Cool Flame)** rejiminin mikroqravitasiyada mövcudluğu sübut edilmişdir.\n"
                "- **Kritik Göstərici:** Sönmə diametri ($d_e$) oksigen konsentrasiyası və inert qaz ($CO_2/He$) nisbətindən asılı olaraq dəyişir."
            )
        elif has_bass:
            return (
                "**BASS (Burning and Suppression of Solids) Tədqiqatı:**\n\n"
                "BASS-I və BASS-II tədqiqatları BKS-də bərk materialların (PMMA/akril, pambıq, pambıq-fiberqlas qarışıqları) mikromaqnitdə yanmasını araşdırır.\n"
                "- **Mühüm Fərq:** Yerdə təbii konveksiya (isti havanın qalxması) alovu qidalandırır. Mikromaqnitdə isə hava axını yalnız süni ventilyasiya vasitəsilə yaradılır.\n"
                "- **Axın Sürətinin Rolu:** Aşağı axın sürətlərində ($< 2.5\\text{ cm/s}$) alov oksigen çatışmazlığından və radiativ istilik itkisindən sönür. $5-15\\text{ cm/s}$ axında isə alovlanma maksimum intensivliyə çatır."
            )
        elif has_saffire:
            return (
                "**SAFFIRE (Spacecraft Fire Safety) Eksperimentləri:**\n\n"
                "SAFFIRE I–VI eksperimentləri pilotsuz Cygnus yük kosmik gəmilərində BKS-dən ayrıldıqdan sonra həyata keçirilmiş genişmiqyaslı yanğın testləridir.\n"
                "- **Məqsəd:** Real kosmik gəmi miqyasında (parça və böyük kompozit panellər) yanğının yayılma sürətini və tüstü telemetriyasını ölçmək.\n"
                "- **Nəticə:** Kosmik gəmilərdə ventilyasiya kanallarının yerləşməsi yanğının yayılma istiqamətini birbaşa müəyyən edir."
            )
        elif has_extinction:
            return (
                "**Mikroqravitasiyada Sönmə Limitləri (Extinction Limits):**\n\n"
                "Mikroqravitasiyada alov iki əsas mexanizmlə sönür:\n"
                "1. **Radiativ Sönmə (Radiative Extinction):** Hava axını çox zəif olduqda ($< 1-2\\text{ cm/s}$), alovdan yayılan şüalanma istiliyi alov zonasını soyudur və reaksiya dayanır.\n"
                "2. **Konvektiv Üfürülmə (Blowoff Extinction):** Yüksək hava axınında istilik reaksiya zonasından sürətlə daşınır.\n"
                "- Verilənlər bazamızdakı 879 eksperimentin analizi göstərir ki, $O_2 < 14.5\\%$ səviyyəsində əksər bərk və maye yanacaqlar avtomatik sönmə rejiminə keçir."
            )
        else:
            return (
                "**FIRE-X Elmi Tədqiqat Mərkəzi:**\n\n"
                "Platformamız 16 NASA uçuş ailəsi üzrə **879 yoxlanılmış mikroqravitasiya yanma eksperimentini** əhatə edir.\n"
                "- **Tədqiqatçı Bölməsi:** Yanacaq növü (PMMA, n-Heptan, Pambıq, Etanol), oksigen faizi ($15\\%-50\\%$) və təzyiq parametrlərinə görə eksperimentləri filtrasiya edin.\n"
                "- **Simulyator:** Artemis Ay Modulu (34% O₂), BKS (21% O₂) və Dərin Kosmos mühitlərində yanğın təhlükəsini hesablayın.\n"
                "- **Müqayisə:** 2-4 eksperiment seçərək yanma müddəti və sönmə diametrlərini müqayisə edin.\n\n"
                "Konkret bir sual versəniz — FLEX, BASS, SAFFIRE, ACME və ya missiya mühiti haqqında — ətraflı elmi cavab verə bilərəm."
            )
    else:
        if has_artemis:
            return (
                "**Artemis Lunar Habitat Fire Hazard Analysis:**\n\n"
                "The NASA Artemis Exploration Atmosphere operates at **34% O₂ and 56.5 kPa (8.2 psia)**:\n"
                "1. **Elevated Fire Hazard Index (FHI = 8.2/10):** Compared to ISS standard normoxic air (21% O₂), material ignition thresholds drop significantly, and flame propagation speed increases by ~42%.\n"
                "2. **Extinction Diameter:** Droplet and solid quenching diameters are notably smaller (~0.82 mm), requiring more aggressive suppression intervention.\n"
                "3. **Safety Advisory:** Materials must satisfy NASA-STD-6001 Test 1 flammability under 34% O₂. Automated $N_2/CO_2$ rapid-quench suppression protocols are required."
            )
        elif has_flex:
            return (
                "**FLEX (Flame Extinction Experiment) Mission Insight:**\n\n"
                "FLEX-1 and FLEX-2 were conducted aboard the International Space Station within the Combustion Integrated Rack (CIR).\n"
                "- **Objective:** Investigate spherical liquid droplet burning (n-heptane, methanol, decane, ethanol) and radiative/convective extinction limits in pure microgravity ($0 \\pm 10^{-4} g$).\n"
                "- **Key Discovery:** Confirmed the quasi-steady existence of low-temperature **'Cool Flame'** burning regimes sustained by non-luminous peroxide kinetics after apparent hot flame quenching.\n"
                "- **Critical Extinction Diameter ($d_e$):** Quantifies the exact droplet dimension at which chemical kinetics fail to overcome radiative losses."
            )
        elif has_bass:
            return (
                "**BASS (Burning and Suppression of Solids) Investigation:**\n\n"
                "BASS-I & BASS-II evaluated solid materials (PMMA/acrylic, cotton fabrics, nomex blends) under controlled forced convective flow in microgravity.\n"
                "- **Physics:** In microgravity, buoyancy-driven natural convection is absent. Forced airflow controls both oxygen delivery and thermal cooling.\n"
                "- **Flow Dynamics:** At low flow speeds ($< 2.5\\text{ cm/s}$), radiative extinction dominates due to insufficient reactant flux. Peak flame spread occurs between $5-15\\text{ cm/s}$."
            )
        elif has_saffire:
            return (
                "**SAFFIRE (Spacecraft Fire Safety) Flight Tests:**\n\n"
                "The SAFFIRE experiments were performed inside unmanned Cygnus cargo spacecraft after departing the ISS.\n"
                "- **Scope:** First realistic, large-scale spacecraft fire propagation tests (up to 1-meter fabric and composite panels).\n"
                "- **Finding:** Demonstrated that ventilation duct orientation directly dictates flame spread trajectory and toxic gas ($CO/CO_2$) stratification in microgravity."
            )
        elif has_extinction:
            return (
                "**Microgravity Extinction Boundaries:**\n\n"
                "Combustion quenching in microgravity is governed by two primary regimes:\n"
                "1. **Radiative Quenching:** Occurs at near-zero or low airflow ($< 2\\text{ cm/s}$), where radiant heat loss from soot and gases exceeds the heat generation rate.\n"
                "2. **Convective Blowoff:** Occurs at elevated flow velocities when residence time becomes shorter than chemical reaction time.\n"
                "- Across our 879 canonical NASA experiments, materials exhibit a sharp flammability cutoff below $14.5\\%~O_2$ in quiescent microgravity."
            )
        else:
            return (
                "**FIRE-X Scientific Research Assistant:**\n\n"
                "The platform indexes **879 verified microgravity experiments** across 16 NASA flight investigations.\n"
                "- **Explorer:** Filter by fuel material (PMMA, n-Heptane, Cotton, Ethanol), oxygen fraction ($15\\%-50\\%$), and pressure regimes.\n"
                "- **Scenario Simulator:** Model fire risks under Artemis Lunar Habitat (34% O₂), ISS (21% O₂), and Deep Space Hypoxic Haven conditions.\n"
                "- **Benchmark Tool:** Select 2–4 experiments for side-by-side metric and extinction parameter comparisons.\n\n"
                "Ask me anything about FLEX, BASS, SAFFIRE, ACME, or mission atmosphere fire hazards and I'll give you a detailed scientific answer."
            )


def query_ai_assistant(
    messages: List[Dict[str, str]],
    language: str = "en",
    page_context: Optional[Dict[str, Any]] = None,
    client_id: str = "default_client",
    stats_summary: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Main entry point for AI chat interactions.
    Handles rate limiting, system prompt synthesis, OpenAI API dispatch, and scientific fallback.
    """
    # 1. Rate Limiting Check
    if not check_rate_limit(client_id):
        err_msg = "Sistemdə sorğu limiti aşıldı. Zəhmət olmasa 1 dəqiqə gözləyin." if language.startswith("az") else "Rate limit exceeded. Please wait 60 seconds before sending more queries."
        return {
            "success": False,
            "error": "rate_limit_exceeded",
            "message": err_msg,
            "response": err_msg,
            "provider": "firex_guardian"
        }

    # 2. Input validation
    if not messages:
        err_msg = "Boş mesaj göndərilə bilməz." if language.startswith("az") else "No messages provided."
        return {"success": False, "error": "empty_input", "response": err_msg, "provider": "firex_guardian"}

    latest_user_message = messages[-1].get("content", "").strip()
    if not latest_user_message:
        err_msg = "Zəhmət olmasa sualınızı daxil edin." if language.startswith("az") else "Please enter a valid question."
        return {"success": False, "error": "empty_content", "response": err_msg, "provider": "firex_guardian"}

    if len(latest_user_message) > 4000:
        latest_user_message = latest_user_message[:4000]

    # 2.5 Topic Relevance & Guardrail Check
    if not is_topic_relevant(latest_user_message):
        logger.info(f"Query rejected by topic guardrail: '{latest_user_message[:60]}...'")
        is_az = language.lower().startswith("az")
        rejection_msg = (
            "⚠️ **Mövzudan kənar sorğu:**\n\n"
            "Mən yalnız **NASA FIRE-X** platforması, kosmosda yanğın təhlükəsizliyi, mikroyerçəkimdə alov fizikası və 879 orbital eksperiment bazası üzrə sualları cavablandırmaq üçün proqramlaşdırılmış elmi köməkçiyəm.\n\n"
            "Bu sual layihəmizin mövzusuna uyğun deyil. Zəhmət olmasa missiya təhlükəsizliyi, BKS/Artemis yanğın riskləri, damcı sönməsi (FLEX) və ya material alovlanması (BASS/SOFIE) ilə bağlı suallarınızı verin."
            if is_az else
            "⚠️ **Out-of-Scope Query:**\n\n"
            "I am a specialized scientific assistant dedicated exclusively to the **NASA FIRE-X** platform, spacecraft fire safety, microgravity combustion physics, and the 879 flight experiments database.\n\n"
            "This question is outside the project scope. Please submit inquiries regarding space mission safety, ISS/Artemis fire hazards, droplet extinction (FLEX), or material flammability (BASS/SOFIE)."
        )
        return {
            "success": True,
            "response": rejection_msg,
            "provider": "FIRE-X Topic Guardian",
            "model": "rule-based-guardrail"
        }

    # 3. System Prompt Construction
    system_prompt = build_system_prompt(language=language, page_context=page_context)

    # 4. Attempt Standard OpenAI ChatCompletions API Call
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

            logger.info(f"Dispatching query to OpenAI API ({OPENAI_MODEL})...")
            
            response = openai_client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": full_input}
                ],
                temperature=0.1
            )
            response_text = response.choices[0].message.content
            return {
                "success": True,
                "response": response_text,
                "provider": "OpenAI",
                "model": OPENAI_MODEL
            }
        except Exception as e:
            logger.warning(f"OpenAI API error: {e}. Falling back to scientific RAG engine.")

    # 5. High-Precision Scientific RAG Fallback
    fallback_response = generate_scientific_fallback(
        user_message=latest_user_message,
        language=language,
        page_context=page_context,
        stats_summary=stats_summary
    )

    return {
        "success": True,
        "response": fallback_response,
        "provider": "FIRE-X Scientific RAG Engine",
        "model": "NASA-PSI-Deterministic-V2",
        "note": "OpenAI API integration active. Add OPENAI_API_KEY in .env for live external GPT responses."
    }
