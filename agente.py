import os
import requests
import google.generativeai as genai

GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]
TEMA = os.environ.get("TEMA", "inteligencia artificial")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

prompt = f"""
Eres un agente de noticias. Busca y analiza las noticias más recientes e importantes sobre: {TEMA}

Responde en este formato exacto:

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

📌 Conclusión del día: ...
"""

response = model.generate_content(prompt)
mensaje = response.text

url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": mensaje})
