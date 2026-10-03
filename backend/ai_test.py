import os
from openai import OpenAI
from dotenv import load_dotenv

# 1. .env faylındakı gizli dəyişənləri sistemə yükləyir
load_dotenv()

# 2. API açarını avtomatik olaraq mühit dəyişənlərindən alır
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_fire_ai_response(user_input):
    try:
        # Yeni və standart OpenAI API sorğu strukturu
        response = client.chat.completions.create(
            model="gpt-4o", # İstəyə görə gpt-3.5-turbo da istifadə edə bilərsən
            messages=[
                {"role": "system", "content": "Sən NASA FIRE-X layihəsi üçün köməkçi elmi süni intellektsən."},
                {"role": "user", "content": user_input}
            ]
        )
        # Gələn cavabın sadəcə mətn hissəsini qaytarır
        return response.choices[0].message.content
    except Exception as e:
        return f"Xəta baş verdi: {e}"

# Test etmək üçün:
if __name__ == "__main__":
    cavab = get_fire_ai_response("write a haiku about ai")
    print(cavab)
