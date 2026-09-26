from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
import sqlite3
import pandas as pd
import os
import json
import random
import difflib
import google.generativeai as genai

app = FastAPI(title="FIRE-X NASA Combustion Platform")

API_KEY = "AQ.Ab8RN6J78I7N2LiVEDN5a-3W74-bMNHILPq4II5XXHib2Oaobw".strip()
genai.configure(api_key=API_KEY)

# RAM-da saxlanılacaq qlobal dəyişənlər
ALL_DF = pd.DataFrame()
ALL_UNIQUE_WORDS = set()

NOT_FOUND_MESSAGES = [
    "Təəssüf ki, verdiyiniz sorğu üzrə NASA Mikrobaza sistemində heç bir uyğun məlumat tapılmadı.",
    "Axtardığınız parametrə uyğun təcrübə qeydi daxil edilməyib. Zəhmət olmasa başqa açar sözlə yoxlayın.",
    "Bazada bu sorğuya dair heç bir yanma təcrübəsi datası mövcud deyil.",
    "Üzr istəyirik, axtardığınız material və ya test kodu sistemdə tapılmadı.",
    "Daxil etdiyiniz sorğu üzrə heç bir eksperiment göstəricisi ashkar olunmadı.",
    "Təəssüf ki, axtarışınız nəticə vermədi. Parametrləri dəqiqləşdirib yenidən cəhd edə bilərsiniz.",
    "Sistemdə bu açar sözə uyğun termal və ya ekstinksiya datası tapılmadı.",
    "Axtarış sorğunuzla üst-üstə düşən hər hansı bir NASA PSI qeydi mövcud deyil.",
    "Təəssüf ki, sorğunuz üzrə bazada heç bir uyğunluq aşkar edilmədi.",
    "Daxil etdiyiniz parametrlər üzrə məlumat bazamız boşdur."
]

@app.on_event("startup")
def load_data_to_ram():
    global ALL_DF, ALL_UNIQUE_WORDS
    conn = sqlite3.connect('nasa_combustion_data.db')
    try:
        flex_df = pd.read_sql("SELECT * FROM flex_data", conn)
        bass_df = pd.read_sql("SELECT * FROM bass_ii_data", conn)
        saffire_df = pd.read_sql("SELECT * FROM saffire_1_data", conn)
        
        ALL_DF = pd.concat([flex_df, bass_df, saffire_df], ignore_index=True).fillna("N/A")
        
        # Unikal sözləri bir dəfə RAM-a yığırıq
        words = set()
        for col in ALL_DF.columns:
            words.update(ALL_DF[col].astype(str).unique())
        ALL_UNIQUE_WORDS = set([w for w in words if len(w) > 2 and w != "N/A"])
        print("Data successfully loaded into RAM!")
    except Exception as e:
        print("Data load error:", e)
    finally:
        conn.close()

class QueryModel(BaseModel):
    question: str

@app.get("/")
def read_root():
    if os.path.exists("frontend/index.html"):
        return FileResponse("frontend/index.html")
    return {"message": "Welcome to FIRE-X"}

@app.post("/api/ask-ai")
def ask_ai(payload: QueryModel):
    raw_query = payload.question.strip()
    normalized_query = raw_query.lower().replace("-", " ")
    query_keywords = [w for w in normalized_query.split() if len(w) > 1]
    
    try:
        all_text = ALL_DF.astype(str)
        
        if query_keywords:
            mask = all_text.apply(lambda row: any(k in " ".join(row).lower() for k in query_keywords), axis=1)
            matching_df = ALL_DF[mask]
        else:
            matching_df = pd.DataFrame()
            
        if not matching_df.empty:
            context_df = matching_df.head(10).copy()
            
            # Tamamilə N/A olan sütunları xaric edirik
            valid_cols = [
                col for col in context_df.columns 
                if not context_df[col].astype(str).str.strip().isin(["N/A", "n/a", "nan", "None", ""]).all()
            ]
            context_df = context_df[valid_cols]
            db_context = context_df.to_dict(orient="records")
            
            model = genai.GenerativeModel('gemini-3.8-flash')
            prompt = f"""
            You are an expert NASA Microgravity Combustion AI assistant for project FIRE-X.
            User asked: "{raw_query}"
            
            Here is the REAL matching data retrieved from our SQLite database:
            {json.dumps(db_context, indent=2)}
            
            Analyze this data and answer the user's question dynamically in Azerbaijani based strictly on this retrieved data.
            Return ONLY a raw JSON object with these keys:
            "report_summary": "A clear 1-2 sentence answer/synthesis in Azerbaijani.",
            "thermal": "Thermal profile insights in Azerbaijani.",
            "extinction": "Extinction dynamics insights in Azerbaijani.",
            "recommendation": "Spacecraft fire safety recommendation in Azerbaijani."
            """
            
            response = model.generate_content(prompt)
            clean_text = response.text.replace('```json', '').replace('```', '').strip()
            ai_data = json.loads(clean_text)
            
            return {
                "query": raw_query,
                "report_summary": ai_data.get("report_summary", "Analiz tamamlandı."),
                "thermal": ai_data.get("thermal", "N/A"),
                "extinction": ai_data.get("extinction", "N/A"),
                "recommendation": ai_data.get("recommendation", "N/A"),
                "did_you_mean": None,
                "rows": db_context
            }
            
        else:
            close_matches = difflib.get_close_matches(raw_query, list(ALL_UNIQUE_WORDS), n=1, cutoff=0.5)
            if not close_matches and query_keywords:
                for kw in query_keywords:
                    matches = difflib.get_close_matches(kw, list(ALL_UNIQUE_WORDS), n=1, cutoff=0.5)
                    if matches:
                        close_matches = matches
                        break
                        
            if close_matches:
                suggested = close_matches[0]
                return {
                    "query": raw_query,
                    "report_summary": "Daxil etdiyiniz sorğuya uyğun dəqiq data tapılmadı.",
                    "thermal": "N/A",
                    "extinction": "N/A",
                    "recommendation": "N/A",
                    "did_you_mean": suggested,
                    "rows": []
                }
            else:
                return {
                    "query": raw_query,
                    "report_summary": random.choice(NOT_FOUND_MESSAGES),
                    "thermal": "N/A",
                    "extinction": "N/A",
                    "recommendation": "N/A",
                    "did_you_mean": None,
                    "rows": []
                }
                
    except Exception as e:
        print("Error:", str(e))
        return {
            "query": raw_query,
            "report_summary": f"Sistem xətası baş verdi: {str(e)}",
            "thermal": "N/A",
            "extinction": "N/A",
            "recommendation": "N/A",
            "did_you_mean": None,
            "rows": []
        }
