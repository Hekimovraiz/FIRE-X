from fastapi import FastAPI
from pydantic import BaseModel
import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

class QueryRequest(BaseModel):
    prompt: str

@app.post("/api/fire-ai")
async def fire_ai_chat(request: QueryRequest):
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system", 
                    "content": (
                        "Sən NASA FIRE-X elmi mütəxəssisisən. İstifadəçinin axtardığı mövzu/material üzrə dərhal JSON formatında cavab ver. "
                        "Cavab dəqiq bu açarlara malik JSON olmalıdır: "
                        "{\n"
                        '  "summary": "Əsas xülasə və tapıntılar",\n'
                        '  "thermal_profile": "Termal və kinetik profil haqqında dinamik məlumat",\n'
                        '  "extinction": "Sönmə dinamikası haqqında məlumat",\n'
                        '  "recommendation": "Kosmik gəmi yanğın təhlükəsizliyi tövsiyəsi"\n'
                        "}\n"
                        "Başqa heç bir mətn yazma, yalnız təmiz JSON qaytar."
                    )
                },
                {"role": "user", "content": request.prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.2
        )
        
        # AI-dan gələn JSON-u parse edirik
        ai_data = json.loads(response.choices[0].message.content)
        return {"status": "success", "data": ai_data}
    
    except Exception as e:
        return {"status": "error", "message": str(e)}
