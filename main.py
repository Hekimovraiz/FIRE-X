from fastapi import FastAPI
from pydantic import BaseModel
import os
from openai import OpenAI
from dotenv import load_dotenv

# .env faylından açarı oxuyuruq
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

# Frontend-dən gələcək məlumatın strukturunu təyin edirik
class QueryRequest(BaseModel):
    prompt: str

@app.post("/api/fire-ai")
async def fire_ai_chat(request: QueryRequest):
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Sən NASA FIRE-X layihəsi üçün köməkçi elmi süni intellektsən. Mikroyerçekimi, yanğın təhlükəsizliyi və kosmik tədqiqatlar üzrə cavablar ver."},
                {"role": "user", "content": request.prompt}
            ]
        )
        ai_reply = response.choices[0].message.content
        return {"status": "success", "response": ai_reply}
    
    except Exception as e:
        return {"status": "error", "message": str(e)}
