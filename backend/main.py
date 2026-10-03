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

class AskAIRequest(BaseModel):
    prompt: str
    language: str = 'en'
    page_context: Optional[Dict[str, Any]] = None


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

@app.post('/api/chat-assistant')
def chat_with_assistant(req: ChatRequest, request: Request):
    client_ip = get_client_ip(request)
    messages_payload = [{'role': m.role, 'content': m.content} for m in req.messages]
    return query_ai_assistant(messages=messages_payload, language=req.language, page_context=req.page_context, client_id=client_ip)

@app.post('/api/ask-ai')
def ask_ai_single_prompt(req: AskAIRequest, request: Request):
    client_ip = get_client_ip(request)
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
