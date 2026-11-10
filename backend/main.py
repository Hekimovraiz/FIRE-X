"""
FIRE-X NASA Microgravity Combustion & Fire Safety API v2.1
Multi-page FastAPI backend with OpenAI Responses API integration.
"""

import os
import logging
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel, Field

from backend.data_service import (
    get_stats, query_experiments, get_experiment_by_id,
    compare_experiments, calculate_mission_scenario, get_investigation_rankings
)
from backend.ai_service import query_ai_assistant

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('firex_api')

app = FastAPI(title='FIRE-X NASA API', version='2.2.0')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'], allow_credentials=True,
    allow_methods=['*'], allow_headers=['*'],
)




BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, 'frontend')
IMAGES_DIR = os.path.join(BASE_DIR, 'images')
HARDWARE_DIR = os.path.join(BASE_DIR, 'hardware')


# Pydantic Models
class CompareRequest(BaseModel):
    experiment_ids: List[str] = Field(..., min_length=1, max_length=4)

class MessageItem(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[MessageItem]
    language: str = 'en'
    page_context: Optional[Dict[str, Any]] = None

class AskAIRequest(BaseModel):
    prompt: str
    language: str = 'en'
    page_context: Optional[Dict[str, Any]] = None

class SensorDataPayload(BaseModel):
    device_id: str = "ESP32-FIREX-01"
    raw_smoke_adc: int = 180
    gas_ppm: float = 45.0
    smoke_density_pct: float = 2.5
    ambient_temp_c: Optional[float] = 23.4
    estimated_o2_pct: Optional[float] = 20.9
    simulated: Optional[bool] = False


# API Routes
@app.get('/api/health')
def health_check():
    return {'status': 'healthy', 'service': 'FIRE-X Space Science API', 'version': '2.2.0', 'canonical_records': 892}

@app.get('/api/stats')
def get_platform_stats():
    try:
        return {'success': True, 'data': get_stats()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/api/experiments')
def get_experiments(
    query: Optional[str] = Query(None), family: Optional[str] = Query(None),
    fuel: Optional[str] = Query(None), outcome: Optional[str] = Query(None),
    min_o2: Optional[float] = Query(None), max_o2: Optional[float] = Query(None),
    page: int = Query(1, ge=1), limit: int = Query(50, ge=1, le=200),
    sort_by: str = Query('experiment_id'), sort_dir: str = Query('ASC')
):
    try:
        return {'success': True, 'data': query_experiments(query=query, family=family, fuel=fuel, outcome=outcome, min_o2=min_o2, max_o2=max_o2, page=page, limit=limit, sort_by=sort_by, sort_dir=sort_dir)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/api/experiments/{experiment_id}')
def get_single_experiment(experiment_id: str):
    try:
        exp = get_experiment_by_id(experiment_id)
        if not exp: raise HTTPException(status_code=404, detail='Experiment not found')
        return {'success': True, 'data': exp}
    except HTTPException: raise
    except Exception as e: raise HTTPException(status_code=500, detail=str(e))

@app.post('/api/compare')
def compare_selected_experiments(req: CompareRequest):
    try:
        return {'success': True, 'data': compare_experiments(req.experiment_ids)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/api/mission-scenario/{scenario_id}')
def get_scenario_metrics(scenario_id: str, custom_o2: Optional[float] = Query(None), custom_pressure: Optional[float] = Query(None)):
    try:
        return {'success': True, 'data': calculate_mission_scenario(scenario_id, custom_o2=custom_o2, custom_pressure=custom_pressure)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/api/investigation-rankings')
def get_rankings_default(environment: str = Query('lunar_habitat')):
    try:
        return {'success': True, 'data': get_investigation_rankings(environment)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/api/investigation-rankings/{environment_id}')
def get_rankings_by_env(environment_id: str):
    try:
        return {'success': True, 'data': get_investigation_rankings(environment_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_client_ip(request: Request) -> str:
    """Extract real client IP considering reverse proxies (Render, Cloudflare, etc.)."""
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    real_ip = request.headers.get("x-real-ip")
    if real_ip:
        return real_ip.strip()
    if request.client and request.client.host:
        return request.client.host
    return "anonymous"


@app.post('/api/chat-assistant')
def chat_with_assistant(req: ChatRequest, request: Request):
    client_ip = get_client_ip(request)
    messages_payload = [{'role': m.role, 'content': m.content} for m in req.messages]
    return query_ai_assistant(messages=messages_payload, language=req.language, page_context=req.page_context, client_id=client_ip)

@app.post('/api/ask-ai')
def ask_ai_single_prompt(req: AskAIRequest, request: Request):
    client_ip = get_client_ip(request)
    return query_ai_assistant(messages=[{'role': 'user', 'content': req.prompt}], language=req.language, page_context=req.page_context, client_id=client_ip)


# ─────────────────────────────────────────────────────────────────────────────
# REAL-TIME IoT HARDWARE ENGINE (ESP32 + MQ-2 GAS & SMOKE SENSOR)
# ─────────────────────────────────────────────────────────────────────────────
import time
import random

LATEST_SENSOR_STATE = {
    "connected": False,
    "last_seen_epoch": 0,
    "device_id": "ESP32-FIREX-01",
    "device_name": "ESP32 NodeMCU + MQ-2 Combustion Sniffer",
    "status": "SEARCHING", # "SEARCHING", "CONNECTING", "ONLINE", "STANDBY", "HAZARD_ALERT"
    "status_az": "Cihaz axtarılır... (ESP32 gözlənilir)",
    "status_en": "Searching for IoT Device... (Awaiting ESP32)",
    "raw_smoke_adc": 0,
    "gas_ppm": 0.0,
    "smoke_density_pct": 0.0,
    "ambient_temp_c": 24.0,
    "estimated_o2_pct": 21.0,
    "fire_hazard_index": 0.0,
    "hazard_level": "STANDBY",
    "hazard_level_az": "GÖZLƏMƏ REJİMİ",
    "advisory_az": "Fiziki ESP32 mikrokontrolleri şəbəkədə axtarılır. Cihazınızı Wi-Fi şəbəkəsinə qoşun.",
    "advisory_en": "Searching for physical ESP32 on network. Power on your device or connect to Wi-Fi.",
    "telemetry_packets_received": 0,
    "is_simulated": False,
    "sim_mode": None,
    "history": []
}

SIM_BASELINES = {
    "connect": {"adc": 185, "gas": 42.0,  "smoke": 3.1,  "temp": 23.6, "o2": 21.0},
    "trigger": {"adc": 1450, "gas": 520.0, "smoke": 64.5, "temp": 28.4, "o2": 21.4},
    "reset":   {"adc": 170, "gas": 38.0,  "smoke": 1.8,  "temp": 23.4, "o2": 20.9},
}

def evaluate_sensor_hazard(gas_ppm: float, smoke_pct: float, o2_pct: float) -> tuple:
    # Scientific FHI calculation driven by live sensor telemetry
    # Formula base: FHI = min(10, 5.1 * (O2/21)^1.5 * (101.3/101.3)^0.4 * Mf) + smoke/gas offset
    x_o2 = (o2_pct if o2_pct else 21.0) / 100.0
    oef = (x_o2 / 0.21) ** 1.5
    fhi_base = 5.1 * oef

    # Gas / smoke hazard adder (MQ-2 sensitivity response)
    # Baseline fresh air: ~20-60 ppm, 0-5% smoke
    # High risk: > 300 ppm, > 30% smoke
    gas_penalty = max(0.0, (gas_ppm - 60.0) / 75.0)
    smoke_penalty = max(0.0, smoke_pct * 0.12)

    fhi = min(10.0, max(1.0, round(fhi_base + gas_penalty + smoke_penalty, 1)))

    if fhi < 3.5:
        lvl = "LOW"
        lvl_az = "AŞAĞI / BOĞULMUŞ"
        adv_az = "Atmosfer sabitdir, yanğın və tüstü hissəcikləri aşkar edilmədi."
        adv_en = "Atmosphere stable, no combustible gas or smoke particles detected."
    elif fhi < 6.8:
        lvl = "NOMINAL"
        lvl_az = "NOMİNAL KOSMİK REJİM"
        adv_az = "Təbii kosmik stansiya fonu. Təhlükəsizlik hədləri daxilindədir."
        adv_en = "Standard spacecraft baseline. All parameters within nominal range."
    elif fhi < 8.8:
        lvl = "ELEVATED"
        lvl_az = "YÜKSƏK HƏYƏCAN (ELEVATED)"
        adv_az = "DİQQƏT: Tüstü/qaz konsentrasiyasında ani sıçrayış! Havalandırma və ventilyasiya təhlil edilir."
        adv_en = "WARNING: Combustible gas / smoke surge detected! Inspecting ventilation loop."
    else:
        lvl = "CRITICAL"
        lvl_az = "KRİTİK YANĞIN TƏHLÜKƏSİ!"
        adv_az = "TƏCİLİ HƏYƏCAN SİQNALI: Alışqan qaz və tüstü konsentrasiyası kritik həddi keçdi! Avtomatik CO₂/N₂ boğma sistemi tövsiyə edilir!"
        adv_en = "CRITICAL EMERGENCY: Smoke & gas density exceeding threshold! Automatic CO₂/N₂ fire suppression recommended!"

    return fhi, lvl, lvl_az, adv_az, adv_en

@app.post('/api/sensor-data')
def receive_iot_sensor_data(payload: SensorDataPayload):
    """
    Endpoint called directly by ESP32 via Wi-Fi HTTP POST (every 1-2 seconds)
    or by the interactive dashboard simulator.
    """
    now = time.time()
    is_sim = bool(payload.simulated)
    if not is_sim:
        LATEST_SENSOR_STATE["sim_mode"] = None

    fhi, lvl, lvl_az, adv_az, adv_en = evaluate_sensor_hazard(
        payload.gas_ppm, payload.smoke_density_pct, payload.estimated_o2_pct or 21.0
    )

    LATEST_SENSOR_STATE["connected"] = True
    LATEST_SENSOR_STATE["is_simulated"] = is_sim
    LATEST_SENSOR_STATE["last_seen_epoch"] = now
    LATEST_SENSOR_STATE["device_id"] = payload.device_id
    
    if is_sim:
        prefix_az = "[TEST DEMO] "
        prefix_en = "[TEST DEMO] "
    else:
        prefix_az = "Fiziki Cihaz: "
        prefix_en = "Physical Device: "

    if lvl in ["ELEVATED", "CRITICAL"]:
        LATEST_SENSOR_STATE["status"] = "HAZARD_ALERT"
        LATEST_SENSOR_STATE["status_az"] = f"{prefix_az}TƏHLÜKƏ SİQNALI (Canlı)"
        LATEST_SENSOR_STATE["status_en"] = f"{prefix_en}HAZARD ALERT (Live)"
    else:
        LATEST_SENSOR_STATE["status"] = "ONLINE"
        LATEST_SENSOR_STATE["status_az"] = f"{prefix_az}Qoşuldu (Canlı Telemetriya)"
        LATEST_SENSOR_STATE["status_en"] = f"{prefix_en}Connected (Live Telemetry)"

    LATEST_SENSOR_STATE["raw_smoke_adc"] = payload.raw_smoke_adc
    LATEST_SENSOR_STATE["gas_ppm"] = round(payload.gas_ppm, 1)
    LATEST_SENSOR_STATE["smoke_density_pct"] = round(payload.smoke_density_pct, 1)
    LATEST_SENSOR_STATE["ambient_temp_c"] = round(payload.ambient_temp_c or 24.0, 1)
    LATEST_SENSOR_STATE["estimated_o2_pct"] = round(payload.estimated_o2_pct or 21.0, 1)
    LATEST_SENSOR_STATE["fire_hazard_index"] = fhi
    LATEST_SENSOR_STATE["hazard_level"] = lvl
    LATEST_SENSOR_STATE["hazard_level_az"] = lvl_az
    LATEST_SENSOR_STATE["advisory_az"] = adv_az
    LATEST_SENSOR_STATE["advisory_en"] = adv_en
    LATEST_SENSOR_STATE["telemetry_packets_received"] += 1

    # Keep rolling 30 data points
    history = LATEST_SENSOR_STATE.get("history", [])
    history.append({
        "timestamp": time.strftime("%H:%M:%S", time.localtime(now)),
        "gas_ppm": round(payload.gas_ppm, 1),
        "smoke_pct": round(payload.smoke_density_pct, 1),
        "fhi": fhi
    })
    if len(history) > 30:
        history.pop(0)
    LATEST_SENSOR_STATE["history"] = history

    return {
        "success": True,
        "message": "Telemetry processed successfully",
        "device_id": payload.device_id,
        "fire_hazard_index": fhi,
        "hazard_level": lvl,
        "is_simulated": is_sim,
        "data": LATEST_SENSOR_STATE
    }

@app.get('/api/sensor-live')
def get_live_sensor_telemetry():
    """
    Called by the Frontend Hardware Dashboard every 1.5 seconds.
    - If in active Demo Simulation mode, generates live streaming telemetry with natural sensor jitter.
    - If in Physical mode and no packet received in last 10 seconds, marks as SEARCHING / STANDBY.
    """
    now = time.time()
    last_seen = LATEST_SENSOR_STATE.get("last_seen_epoch", 0)
    sim_mode = LATEST_SENSOR_STATE.get("sim_mode")

    if LATEST_SENSOR_STATE.get("is_simulated") and sim_mode in SIM_BASELINES:
        if now - last_seen >= 1.1:
            base = SIM_BASELINES[sim_mode]
            if sim_mode == "trigger":
                adc_jitter = random.randint(-45, 55)
                gas_jitter = random.uniform(-18.0, 22.0)
                smoke_jitter = random.uniform(-2.5, 3.2)
            else:
                adc_jitter = random.randint(-6, 7)
                gas_jitter = random.uniform(-1.6, 1.8)
                smoke_jitter = random.uniform(-0.25, 0.3)

            payload = SensorDataPayload(
                device_id="ESP32-DEMO-SIMULATOR",
                raw_smoke_adc=max(80, min(4095, base["adc"] + adc_jitter)),
                gas_ppm=max(15.0, round(base["gas"] + gas_jitter, 1)),
                smoke_density_pct=max(0.4, min(100.0, round(base["smoke"] + smoke_jitter, 1))),
                ambient_temp_c=round(base["temp"] + random.uniform(-0.15, 0.15), 1),
                estimated_o2_pct=base["o2"],
                simulated=True
            )
            receive_iot_sensor_data(payload)
        return {
            "success": True,
            "data": LATEST_SENSOR_STATE
        }

    # Auto-disconnect physical device if no live packets received in last 10 seconds
    if (now - last_seen > 10.0 or last_seen == 0) and LATEST_SENSOR_STATE["connected"]:
        LATEST_SENSOR_STATE["connected"] = False
        LATEST_SENSOR_STATE["is_simulated"] = False
        LATEST_SENSOR_STATE["sim_mode"] = None
        LATEST_SENSOR_STATE["status"] = "SEARCHING"
        LATEST_SENSOR_STATE["status_az"] = "Cihaz axtarılır... (ESP32 gözlənilir)"
        LATEST_SENSOR_STATE["status_en"] = "Searching for IoT Device... (Awaiting ESP32)"
        LATEST_SENSOR_STATE["gas_ppm"] = 0.0
        LATEST_SENSOR_STATE["smoke_density_pct"] = 0.0
        LATEST_SENSOR_STATE["raw_smoke_adc"] = 0
        LATEST_SENSOR_STATE["fire_hazard_index"] = 0.0
        LATEST_SENSOR_STATE["hazard_level"] = "STANDBY"
        LATEST_SENSOR_STATE["hazard_level_az"] = "GÖZLƏMƏ REJİMİ"
        LATEST_SENSOR_STATE["advisory_az"] = "Fiziki ESP32 mikrokontrolleri axtarılır. Cihazınızı Wi-Fi şəbəkəsinə qoşun."
        LATEST_SENSOR_STATE["advisory_en"] = "Searching for physical ESP32 on network. Power on your device or connect to Wi-Fi."

    return {
        "success": True,
        "data": LATEST_SENSOR_STATE
    }

@app.post('/api/sensor-simulate')
def simulate_sensor_telemetry(action: str = Query("trigger", pattern="^(trigger|reset|connect|disconnect)$")):
    """
    Explicit demo button trigger for presentations (when physical ESP32 is not connected):
    - 'connect': Starts live demo baseline telemetry stream
    - 'trigger': Simulates smoke / gas surge stream
    - 'reset': Restores clean air baseline stream
    - 'disconnect': Immediately resets everything back to SEARCHING / STANDBY
    """
    if action == "disconnect":
        LATEST_SENSOR_STATE["connected"] = False
        LATEST_SENSOR_STATE["is_simulated"] = False
        LATEST_SENSOR_STATE["sim_mode"] = None
        LATEST_SENSOR_STATE["last_seen_epoch"] = 0
        LATEST_SENSOR_STATE["status"] = "SEARCHING"
        LATEST_SENSOR_STATE["status_az"] = "Cihaz axtarılır... (ESP32 gözlənilir)"
        LATEST_SENSOR_STATE["status_en"] = "Searching for IoT Device... (Awaiting ESP32)"
        LATEST_SENSOR_STATE["gas_ppm"] = 0.0
        LATEST_SENSOR_STATE["smoke_density_pct"] = 0.0
        LATEST_SENSOR_STATE["raw_smoke_adc"] = 0
        LATEST_SENSOR_STATE["fire_hazard_index"] = 0.0
        LATEST_SENSOR_STATE["hazard_level"] = "STANDBY"
        LATEST_SENSOR_STATE["hazard_level_az"] = "GÖZLƏMƏ REJİMİ"
        LATEST_SENSOR_STATE["advisory_az"] = "Fiziki ESP32 mikrokontrolleri axtarılır. Cihazınızı Wi-Fi şəbəkəsinə qoşun."
        LATEST_SENSOR_STATE["advisory_en"] = "Searching for physical ESP32 on network. Power on your device or connect to Wi-Fi."
        LATEST_SENSOR_STATE["telemetry_packets_received"] = 0
        LATEST_SENSOR_STATE["history"] = []
        return {"success": True, "action": action, "data": LATEST_SENSOR_STATE}

    LATEST_SENSOR_STATE["sim_mode"] = action
    baseline = SIM_BASELINES.get(action, SIM_BASELINES["connect"])

    # Seed initial history if fewer than 4 points so chart renders immediately on first click
    now = time.time()
    history = LATEST_SENSOR_STATE.get("history", [])
    if len(history) < 4:
        seed_fhi, _, _, _, _ = evaluate_sensor_hazard(baseline["gas"], baseline["smoke"], baseline["o2"])
        for i in range(4, 0, -1):
            t_str = time.strftime("%H:%M:%S", time.localtime(now - i * 1.5))
            history.append({
                "timestamp": t_str,
                "gas_ppm": round(baseline["gas"] + random.uniform(-1.5, 1.5), 1),
                "smoke_pct": round(baseline["smoke"] + random.uniform(-0.2, 0.2), 1),
                "fhi": seed_fhi
            })
        LATEST_SENSOR_STATE["history"] = history

    payload = SensorDataPayload(
        device_id="ESP32-DEMO-SIMULATOR",
        raw_smoke_adc=baseline["adc"],
        gas_ppm=baseline["gas"],
        smoke_density_pct=baseline["smoke"],
        ambient_temp_c=baseline["temp"],
        estimated_o2_pct=baseline["o2"],
        simulated=True
    )
    result = receive_iot_sensor_data(payload)
    result["action"] = action
    return result


# Static files
if os.path.exists(IMAGES_DIR):
    app.mount('/images', StaticFiles(directory=IMAGES_DIR), name='images')

if os.path.exists(FRONTEND_DIR):
    app.mount('/static', StaticFiles(directory=FRONTEND_DIR), name='static')


# Multi-page HTML routes
PAGE_MAP = {
    '/': 'index.html',
    '/analytics': 'analytics.html',
    '/explorer': 'explorer.html',
    '/simulator': 'simulator.html',
    '/hardware': 'hardware.html',
    '/ai': 'ai.html',
    '/about': 'about.html',
}

def serve_page(filename: str):
    no_cache = {"Cache-Control": "no-cache, no-store, must-revalidate"}
    path = os.path.join(FRONTEND_DIR, filename)
    if os.path.exists(path):
        return FileResponse(path, media_type='text/html', headers=no_cache)
    # Fallback to index
    index = os.path.join(FRONTEND_DIR, 'index.html')
    if os.path.exists(index):
        return FileResponse(index, media_type='text/html', headers=no_cache)
    return JSONResponse({'error': 'Page not found'}, status_code=404)

@app.get('/favicon.ico')
def favicon():
    favicon_path = os.path.join(IMAGES_DIR, 'Fire-X.jpeg')
    if os.path.exists(favicon_path):
        return FileResponse(favicon_path, media_type='image/jpeg')
    return JSONResponse({'error': 'Favicon not found'}, status_code=404)

@app.get('/')
def home(): return serve_page('index.html')

@app.get('/analytics')
def analytics(): return serve_page('analytics.html')

@app.get('/explorer')
def explorer(): return serve_page('explorer.html')

@app.get('/simulator')
def simulator(): return serve_page('simulator.html')

@app.get('/hardware')
def hardware_page(): return serve_page('hardware.html')

@app.get('/hardware/3d-viewer')
@app.get('/hardware/3d_viewer.html')
def serve_hardware_3d_viewer():
    fpath = os.path.join(HARDWARE_DIR, '3d_viewer.html')
    if os.path.exists(fpath):
        return FileResponse(fpath, media_type='text/html', headers={'Cache-Control': 'no-cache, no-store, must-revalidate', 'Content-Disposition': 'inline'})
    raise HTTPException(status_code=404, detail='3D Viewer not found')

@app.get('/hardware/{filename}')
def hardware_file_download(filename: str):
    safe_name = os.path.basename(filename)
    fpath = os.path.join(HARDWARE_DIR, safe_name)
    if os.path.exists(fpath):
        if safe_name.endswith('.html'):
            return FileResponse(fpath, media_type='text/html', headers={'Cache-Control': 'no-cache', 'Content-Disposition': 'inline'})
        return FileResponse(fpath, filename=safe_name)
    raise HTTPException(status_code=404, detail='Hardware file not found')

@app.get('/ai')
def ai_assistant(): return serve_page('ai.html')

@app.get('/about')
def about(): return serve_page('about.html')



if __name__ == '__main__':
    import uvicorn
    uvicorn.run('backend.main:app', host='0.0.0.0', port=8000, reload=True)
