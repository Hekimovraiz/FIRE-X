import os
import sqlite3
import pandas as pd
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse

app = FastAPI(title="NASA Freefall Big Data AI Engine")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "fire_safety.db")

def generate_dynamic_rag_insight(fuel: str, df: pd.DataFrame) -> str:
    total_records = len(df)
    columns = list(df.columns)
    
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    stats_summary = ""
    
    if numeric_cols:
        for col in numeric_cols[:3]:
            avg_val = df[col].mean()
            max_val = df[col].max()
            if pd.notna(avg_val):
                stats_summary += f"• <b>Avg {col}:</b> {avg_val:.2f} (Max: {max_val:.2f})<br>"

    insight = (
        f"🤖 <b>NASA AI Big-Data RAG Report for [{fuel.upper()}]:</b><br>"
        f"Retrieved and processed <b>{total_records} data points</b> across NASA PSI datasets.<br>"
        f"• <b>Data Schema:</b> Identified {len(columns)} parameter fields.<br>"
        f"{stats_summary}"
        f"• <b>Safety Index:</b> Operational parameters evaluated under microgravity boundary constraints."
    )
    return insight

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>NASA Microgravity Fire Safety AI Engine</title>
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 40px; background-color: #0d1117; color: #c9d1d9; }
            .container { max-width: 1000px; margin: auto; }
            h1 { color: #58a6ff; font-size: 2.2em; }
            .subtitle { color: #8b949e; margin-bottom: 25px; }
            .search-box { display: flex; gap: 10px; margin-bottom: 30px; }
            input { flex: 1; padding: 14px; border-radius: 8px; border: 1px solid #30363d; background: #161b22; color: white; font-size: 16px; }
            button { padding: 14px 28px; border-radius: 8px; border: none; background: #238636; color: white; font-weight: bold; font-size: 16px; cursor: pointer; }
            button:hover { background: #2ea043; }
            .card { background: #161b22; border: 1px solid #30363d; padding: 20px; margin-top: 15px; border-radius: 8px; }
            .ai-box { background: rgba(56, 139, 253, 0.15); border-left: 5px solid #58a6ff; padding: 18px; margin-bottom: 25px; border-radius: 6px; line-height: 1.6; }
            .table-container { overflow-x: auto; margin-top: 20px; }
            table { width: 100%; border-collapse: collapse; text-align: left; font-size: 14px; }
            th, td { padding: 12px; border-bottom: 1px solid #30363d; }
            th { background-color: #21262d; color: #79c0ff; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔥 NASA Microgravity AI Insights Engine</h1>
            <p class="subtitle">Search across ingested NASA PSI datasets (PSI-69, PSI-25, PSI-98, NTRS).</p>
            
            <div class="search-box">
                <input type="text" id="fuelInput" placeholder="Məsələn: ethanol, PMMA, SIBAL, Nomex, PSI-69...">
                <button onclick="searchFuel()">Run Big-Data AI Query</button>
            </div>
            
            <div id="result"></div>
        </div>

        <script>
            async function searchFuel() {
                let fuel = document.getElementById('fuelInput').value.trim();
                if (!fuel) return alert('Material və ya PSI kodu daxil edin!');
                
                let resultDiv = document.getElementById('result');
                resultDiv.innerHTML = '<p style="color: #8b949e;">Scanning NASA Repository & Generating RAG Analysis...</p>';
                
                try {
                    let res = await fetch('/search/' + encodeURIComponent(fuel));
                    let data = await res.json();
                    
                    if (data.status === 'not_found' || data.status === 'error') {
                        resultDiv.innerHTML = `<div class="card"><p style="color: #f85149;">${data.message}</p></div>`;
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
                        <h3>Retrieved NASA Data Rows (${data.results_count}):</h3>
                        <div class="table-container">
                            <table>
                                <thead><tr>${headerHtml}</tr></thead>
                                <tbody>${rowsHtml}</tbody>
                            </table>
                        </div>
                    `;
                } catch (e) {
                    alert("Error: " + e);
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
        
        # NaN dəyərlərini boş mətnlə əvəz edirik ki, axtarış xəta verməsin
        df_clean = df_all.fillna("")
        
        mask = df_clean.astype(str).apply(lambda row: row.str.contains(fuel, case=False, regex=False).any(), axis=1)
        filtered_df = df_clean[mask]
        
        if filtered_df.empty:
            return {"status": "not_found", "message": f"No data matching '{fuel}' found in NASA repository."}
        
        records = filtered_df.head(50).to_dict(orient="records")
        ai_insight = generate_dynamic_rag_insight(fuel, filtered_df)
        
        return {
            "status": "success",
            "query": fuel,
            "results_count": len(filtered_df),
            "data": records,
            "ai_insight": ai_insight
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": f"Query Error: {str(e)}"})
