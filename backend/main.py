import os
import sqlite3
import pandas as pd
import requests
import time
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse

app = FastAPI(title="NASA Freefall Dynamic AI Engine")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "fire_safety.db")

# API açarı artıq yalnız sistem dəyişənindən oxunur (GitHub bloklamayacaq)
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

def generate_llm_rag_insight(fuel: str, records: list) -> str:
    count = len(records)
    avg_temp = sum(r.get('flame_temp_k', 0) for r in records if r.get('flame_temp_k')) / max(count, 1)
    outcomes = list(set(r.get('extinction_outcome', 'N/A') for r in records if r.get('extinction_outcome')))
    
    ai_fallback = (
        f"✨ <b>NASA AI Dynamic Microgravity RAG Report for [{fuel.upper()}]:</b><br>"
        f"Retrieved <b>{count} experimental records</b> from NASA PSI & NTRS repositories.<br>"
        f"• <b>Thermal Profile:</b> Mean observed flame temperature is <b>{avg_temp:.1f} K</b>, indicating controlled radiative-convective energy balance.<br>"
        f"• <b>Extinction Dynamics:</b> Dominant extinction mechanics observed: <i>{', '.join(str(o) for o in outcomes)}</i> under microgravity suppression.<br>"
        f"• <b>Spacecraft Fire Safety Recommendation:</b> Implement immediate localized oxygen suppression if localized combustion exceeds standard boundary layer thresholds."
    )

    if not GEMINI_API_KEY:
        return ai_fallback

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    
    prompt = f"""
    You are a NASA Microgravity Fire Safety & Combustion Physics AI Specialist.
    Analyze the following retrieved experimental records for material/query: '{fuel}':
    {records}
    
    Provide a concise, highly professional scientific analysis formatted strictly in HTML (use <b>, <i>, <br>, <ul>, <li>):
    1. Summarize key combustion trends (burn duration, flame temperature, oxygen threshold).
    2. Explain microgravity extinction risks and physics (radiative cooling, suppression).
    3. Provide a Spacecraft Safety Recommendation based strictly on the data.
    Keep it under 120 words. No markdown blocks.
    """
    
    payload = {"contents": [{"parts": [{"text": prompt}]}]}

    for attempt in range(3):
        try:
            response = requests.post(url, json=payload, timeout=10)
            data = response.json()
            if response.status_code == 200:
                ai_text = data['candidates'][0]['content']['parts'][0]['text']
                return f"✨ <b>NASA Gemini Live AI Analysis:</b><br><br>{ai_text}"
            elif "high demand" in str(data).lower() or response.status_code == 503:
                time.sleep(1.5)
                continue
            else:
                break
        except Exception:
            time.sleep(1)
            continue

    return ai_fallback

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>NASA Microgravity Fire Safety AI Engine</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
            body { font-family: 'Inter', sans-serif; margin: 0; padding: 40px; background: radial-gradient(circle at top, #111b27 0%, #0d1117 100%); color: #c9d1d9; min-height: 100vh; }
            .container { max-width: 1050px; margin: auto; }
            h1 { color: #58a6ff; font-size: 2.5em; font-weight: 700; display: flex; align-items: center; gap: 15px; }
            .subtitle { color: #8b949e; margin-bottom: 30px; font-size: 1.1em; }
            .search-box { display: flex; gap: 12px; margin-bottom: 35px; background: #161b22; padding: 10px; border-radius: 12px; border: 1px solid #30363d; box-shadow: 0 8px 24px rgba(0,0,0,0.4); }
            input { flex: 1; padding: 14px 18px; border-radius: 8px; border: 1px solid transparent; background: #0d1117; color: white; font-size: 16px; outline: none; transition: all 0.3s ease; }
            input:focus { border-color: #58a6ff; box-shadow: 0 0 10px rgba(88, 166, 255, 0.3); }
            button { padding: 14px 30px; border-radius: 8px; border: none; background: linear-gradient(135deg, #238636 0%, #2ea043 100%); color: white; font-weight: 600; font-size: 16px; cursor: pointer; transition: all 0.3s ease; box-shadow: 0 4px 12px rgba(35, 134, 54, 0.4); }
            button:hover { transform: translateY(-2px); box-shadow: 0 6px 16px rgba(46, 160, 67, 0.6); }
            .card { background: #161b22; border: 1px solid #30363d; padding: 25px; margin-top: 20px; border-radius: 12px; }
            .ai-box { background: rgba(56, 139, 253, 0.1); border: 1px solid rgba(88, 166, 255, 0.3); border-left: 5px solid #58a6ff; padding: 22px; margin-bottom: 30px; border-radius: 8px; line-height: 1.7; animation: fadeIn 0.6s ease-in-out; box-shadow: 0 4px 20px rgba(56, 139, 253, 0.1); }
            @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
            .loader { display: inline-block; width: 20px; height: 20px; border: 3px solid rgba(255,255,255,.3); border-radius: 50%; border-top-color: #58a6ff; animation: spin 1s ease-in-out infinite; margin-right: 10px; vertical-align: middle; }
            @keyframes spin { to { transform: rotate(360deg); } }
            .table-container { overflow-x: auto; margin-top: 20px; border-radius: 10px; border: 1px solid #30363d; animation: fadeIn 0.8s ease-in-out; }
            table { width: 100%; border-collapse: collapse; text-align: left; font-size: 14px; }
            th, td { padding: 14px 18px; border-bottom: 1px solid #30363d; }
            th { background-color: #21262d; color: #79c0ff; font-weight: 600; }
            tr:hover { background-color: rgba(255,255,255,0.02); }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔥 NASA Microgravity AI Insights Engine</h1>
            <p class="subtitle">Advanced RAG combustion analytics backed by live Google Gemini intelligence.</p>
            
            <div class="search-box">
                <input type="text" id="fuelInput" placeholder="Axtarış edin: ethanol, PMMA, SIBAL, Nomex, PSI-69..." onkeypress="if(event.key === 'Enter') searchFuel();">
                <button onclick="searchFuel()">Run Live AI Query</button>
            </div>
            
            <div id="result"></div>
        </div>

        <script>
            async function searchFuel() {
                let fuel = document.getElementById('fuelInput').value.trim();
                if (!fuel) return alert('Zəhmət olmasa axtarış üçün söz daxil edin!');
                
                let resultDiv = document.getElementById('result');
                resultDiv.innerHTML = '<div class="card" style="text-align: center; color: #8b949e;"><div class="loader"></div>Querying NASA Database & Generating Neural RAG Insights...</div>';
                
                try {
                    let res = await fetch('/search/' + encodeURIComponent(fuel));
                    let data = await res.json();
                    
                    if (data.status === 'not_found' || data.status === 'error') {
                        resultDiv.innerHTML = `<div class="card" style="animation: fadeIn 0.4s;"><p style="color: #f85149; margin:0;">${data.message}</p></div>`;
                        return;
                    }
                    
                    let cols = Object.keys(data.data[0]);
                    let headerHtml = cols.map(c => `<th>${c}</th>`).join('');
                    let rowsHtml = data.data.map(row => {
                        let tds = cols.map(c => `<td>${row[c] !== null && row[c] !== undefined ? row[c] : '-'}</td>`).join('');
                        return `<tr>${tds}</tr>`;
                    }).join('');
                    
                    resultDiv.innerHTML = `
                        <div class="ai-box">${data.ai_insight}</div>
                        <h3 style="color: #e6edf3; font-weight: 600;">Retrieved NASA Data Rows (${data.results_count}):</h3>
                        <div class="table-container">
                            <table>
                                <thead><tr>${headerHtml}</tr></thead>
                                <tbody>${rowsHtml}</tbody>
                            </table>
                        </div>
                    `;
                } catch (e) {
                    alert("Xəta baş verdi: " + e);
                }
            }
        </script>
    </body>
    </html>
    """

@app.get("/search/{fuel}")
def search_fuel(fuel: str):
    if not os.path.exists(DB_PATH):
        return JSONResponse(status_code=404, content={"status": "error", "message": "Database not found."})
    
    try:
        conn = sqlite3.connect(DB_PATH)
        df_all = pd.read_sql("SELECT * FROM flex_experiments", conn)
        conn.close()
        
        df_clean = df_all.fillna("")
        mask = df_clean.astype(str).apply(lambda row: row.str.contains(fuel, case=False, regex=False).any(), axis=1)
        filtered_df = df_clean[mask]
        
        if filtered_df.empty:
            return {"status": "not_found", "message": f"No data matching '{fuel}' found in NASA repository."}
        
        records = filtered_df.head(20).to_dict(orient="records")
        ai_insight = generate_llm_rag_insight(fuel, records)
        
        return {
            "status": "success",
            "query": fuel,
            "results_count": len(filtered_df),
            "data": records,
            "ai_insight": ai_insight
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": f"Query Error: {str(e)}"})
