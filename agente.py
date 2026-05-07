import os
import requests

GROQ_API_KEY = os.environ["GROQ_API_KEY"]
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

url = "https://api.groq.com/openai/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

body = {
    "model": "llama-3.3-70b-versatile",
    "messages": [{"role": "user", "content": prompt}]
}

r = requests.post(url, headers=headers, json=body)
data = r.json()
mensaje = data["choices"][0]["message"]["content"]

telegram_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
requests.post(telegram_url, data={"chat_id": TELEGRAM_CHAT_ID, "text": mensaje})
