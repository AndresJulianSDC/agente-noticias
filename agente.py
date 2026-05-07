import os
import requests

GROQ_API_KEY = os.environ["GROQ_API_KEY"]
TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]
NEWS_API_KEY = os.environ["NEWS_API_KEY"]

# Buscar noticias en inglés
query = "electricity energy gas natural Colombia Guatemala Panama Mexico Ecuador"
news_url = f"https://newsapi.org/v2/everything?q={query}&sortBy=publishedAt&pageSize=5&apiKey={NEWS_API_KEY}"

r = requests.get(news_url)
data = r.json()
articulos = data.get("articles", [])
print("Respuesta NewsAPI:", data.get("status"), "- Total:", data.get("totalResults"), "- Error:", data.get("message"))

if not articulos:
    mensaje = "⚠️ No se encontraron noticias hoy sobre energía en los mercados de la región."
    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(telegram_url, data={"chat_id": TELEGRAM_CHAT_ID, "text": mensaje})
    exit()

contexto = ""
links = []
for i, art in enumerate(articulos, 1):
    titulo = art.get("title") or ""
    fuente = art["source"].get("name") or ""
    descripcion = art.get("description") or ""
    url = art.get("url") or ""
    contexto += f"\nNoticia {i}:\nTítulo: {titulo}\nFuente: {fuente}\nDescripción: {descripcion}\nURL: {url}\n"
    links.append(f"🔗 {titulo}\n{url}")

prompt = f"""Eres un analista experto en mercados de energía eléctrica y gas natural en Latinoamérica.
Las siguientes noticias están en inglés. Tradúcelas, analízalas y explica su impacto en los mercados regulados y no regulados de Colombia, Guatemala, Panamá, México y Ecuador.

{contexto}

Responde en español con este formato:

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

links_texto = "\n\n🔗 FUENTES:\n" + "\n\n".join(links)
mensaje_final = analisis + links_texto

if len(mensaje_final) > 4096:
    mensaje_final = mensaje_final[:4090] + "..."

telegram_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
requests.post(telegram_url, data={"chat_id": TELEGRAM_CHAT_ID, "text": mensaje_final})
