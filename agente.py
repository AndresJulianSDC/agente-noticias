import os
import requests

GROQ_API_KEY = os.environ["GROQ_API_KEY"]
TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]
NEWS_API_KEY = os.environ["NEWS_API_KEY"]

# Buscar noticias reales
query = "energia electrica gas natural Colombia Guatemala Panama Mexico Ecuador mercado regulado"
news_url = f"https://newsapi.org/v2/everything?q={query}&language=es&sortBy=publishedAt&pageSize=5&apiKey={NEWS_API_KEY}"

r = requests.get(news_url)
articulos = r.json().get("articles", [])

if not articulos:
    mensaje = "⚠️ No se encontraron noticias hoy sobre energía en los mercados de la región."
    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(telegram_url, data={"chat_id": TELEGRAM_CHAT_ID, "text": mensaje})
    exit()

# Preparar contexto para Groq
contexto = ""
links = []
for i, art in enumerate(articulos, 1):
    contexto += f"\nNoticia {i}:\nTítulo: {art['title']}\nFuente: {art['source']['name']}\nDescripción: {art['description']}\nURL: {art['url']}\n"
    links.append(f"🔗 {art['title']}\n{art['url']}")

prompt = f"""Eres un analista experto en mercados de energía eléctrica y gas natural en Latinoamérica.
Analiza estas noticias reales y explica su impacto en los mercados regulados y no regulados de Colombia, Guatemala, Panamá, México y Ecuador.

{contexto}

Responde en este formato:

📰 RESUMEN ENERGÉTICO DEL DÍA

🔹 Noticia 1:
Título: ...
Fuente: ...
Impacto mercado regulado: ...
Impacto mercado no regulado: ...
¿Qué debes saber?: ...

(repite para cada noticia)

📌 Conclusión del día: ..."""

groq_url = "https://api.groq.com/openai/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}
body = {
    "model": "llama-3.3-70b-versatile",
    "messages": [{"role": "user", "content": prompt}]
}

r = requests.post(groq_url, headers=headers, json=body)
analisis = r.json()["choices"][0]["message"]["content"]

# Agregar links al final
links_texto = "\n\n🔗 FUENTES:\n" + "\n\n".join(links)
mensaje_final = analisis + links_texto

# Telegram tiene límite de 4096 caracteres
if len(mensaje_final) > 4096:
    mensaje_final = mensaje_final[:4090] + "..."

telegram_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
requests.post(telegram_url, data={"chat_id": TELEGRAM_CHAT_ID, "text": mensaje_final})
