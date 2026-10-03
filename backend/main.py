"""
FIRE-X NASA Microgravity Combustion & Fire Safety API v2.1
Multi-page FastAPI backend with OpenAI Responses API integration.
"""

import os
import time
import random
import hmac
import hashlib
import logging
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel, Field

from backend.data_service import (
    get_stats, query_experiments, get_experiment_by_id,
    compare_experiments, calculate_mission_scenario
)
from backend.ai_service import query_ai_assistant

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('firex_api')

app = FastAPI(title='FIRE-X NASA API', version='2.1.0')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'], allow_credentials=True,
    allow_methods=['*'], allow_headers=['*'],
)


CAPTCHA_SECRET = os.getenv("CAPTCHA_SECRET", "firex_space_apps_secure_key_2026")

def generate_captcha_challenge():
    a = random.randint(3, 19)
    b = random.randint(2, 9)
    ans = a + b
    timestamp = int(time.time())
    sig = hmac.new(CAPTCHA_SECRET.encode(), f"{ans}:{timestamp}".encode(), hashlib.sha256).hexdigest()
    return {
        "question": f"{a} + {b} = ?",
        "challenge_token": f"{sig}.{timestamp}"
    }

def verify_captcha_solution(solution: str, challenge_token: str) -> bool:
    try:
        if not solution or not challenge_token or "." not in challenge_token:
            return False
        sig, ts_str = challenge_token.split(".", 1)
        ts = int(ts_str)
        # Token valid for 10 minutes (600 seconds)
        if time.time() - ts > 600 or time.time() < ts - 10:
            return False
        sol_clean = solution.strip()
        expected_sig = hmac.new(CAPTCHA_SECRET.encode(), f"{sol_clean}:{ts}".encode(), hashlib.sha256).hexdigest()
        return hmac.compare_digest(sig, expected_sig)
    except Exception:
        return False

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, 'frontend')
IMAGES_DIR = os.path.join(BASE_DIR, 'images')


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
    captcha_solution: Optional[str] = None
    captcha_token: Optional[str] = None

class AskAIRequest(BaseModel):
    prompt: str
    language: str = 'en'
    page_context: Optional[Dict[str, Any]] = None
    captcha_solution: Optional[str] = None
    captcha_token: Optional[str] = None


# API Routes
@app.get('/api/health')
def health_check():
    return {'status': 'healthy', 'service': 'FIRE-X Space Science API', 'version': '2.1.0', 'canonical_records': 879}

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


@app.get('/api/captcha')
def get_captcha():
    return {"success": True, "data": generate_captcha_challenge()}

@app.post('/api/chat-assistant')
def chat_with_assistant(req: ChatRequest, request: Request):
    client_ip = get_client_ip(request)
    
    # Verify Captcha
    if not verify_captcha_solution(req.captcha_solution or "", req.captcha_token or ""):
        err_msg = "Təhlükəsizlik yoxlaması (CAPTCHA) uğursuz oldu və ya vaxtı bitdi. Zəhmət olmasa yenidən cəhd edin." if req.language.startswith("az") else "Security verification (CAPTCHA) failed or expired. Please solve the security check."
        return {
            "success": False,
            "error": "captcha_failed",
            "response": err_msg,
            "provider": "FIRE-X Security Firewall",
            "require_captcha": True
        }

    messages_payload = [{'role': m.role, 'content': m.content} for m in req.messages]
    return query_ai_assistant(messages=messages_payload, language=req.language, page_context=req.page_context, client_id=client_ip)

@app.post('/api/ask-ai')
def ask_ai_single_prompt(req: AskAIRequest, request: Request):
    client_ip = get_client_ip(request)
    
    # Verify Captcha if provided or enforce
    if req.captcha_token and not verify_captcha_solution(req.captcha_solution or "", req.captcha_token or ""):
        err_msg = "CAPTCHA yoxlaması uğursuz oldu." if req.language.startswith("az") else "CAPTCHA verification failed."
        return {"success": False, "error": "captcha_failed", "response": err_msg, "require_captcha": True}

    return query_ai_assistant(messages=[{'role': 'user', 'content': req.prompt}], language=req.language, page_context=req.page_context, client_id=client_ip)



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
    '/ai': 'ai.html',
    '/about': 'about.html',
}

def serve_page(filename: str):
    path = os.path.join(FRONTEND_DIR, filename)
    if os.path.exists(path):
        return FileResponse(path, media_type='text/html')
    # Fallback to index
    index = os.path.join(FRONTEND_DIR, 'index.html')
    if os.path.exists(index):
        return FileResponse(index, media_type='text/html')
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

@app.get('/ai')
def ai_assistant(): return serve_page('ai.html')

@app.get('/about')
def about(): return serve_page('about.html')


if __name__ == '__main__':
    import uvicorn
    uvicorn.run('backend.main:app', host='0.0.0.0', port=8000, reload=True)
