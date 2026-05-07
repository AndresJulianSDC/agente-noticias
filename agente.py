import os
import requests

GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]
TEMA = os.environ.get("TEMA", "inteligencia artificial")

prompt = f"""Eres un agente de noticias. Analiza y resume las noticias más recientes e importantes sobre: {TEMA}

Responde en este formato:

📰 RESUMEN DEL DÍA — {TEMA.upper()}

🔹 Noticia 1:
Título: ...
Fuente: ...
Resumen: ...
¿Qué debes saber?: ...

🔹 Noticia 2:
Título: ...
Fuente: ...
Resumen: ...
¿Qué debes saber?: ...

🔹 Noticia 3:
Título: ...
Fuente: ...
Resumen: ...
¿Qué debes saber?: ...

📌 Conclusión del día: ..."""

url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

body = {
    "contents": [{"parts": [{"text": prompt}]}]
}

r = requests.post(url, json=body)
data = r.json()
print(data)
if "candidates" not in data:
    raise Exception(f"Error de Gemini: {data}")
mensaje = data["candidates"][0]["content"]["parts"][0]["text"]
telegram_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
requests.post(telegram_url, data={"chat_id": TELEGRAM_CHAT_ID, "text": mensaje})
