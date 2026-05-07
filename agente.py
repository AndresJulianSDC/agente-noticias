import os
import requests

GROQ_API_KEY = os.environ["GROQ_API_KEY"]
TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]
GNEWS_API_KEY = os.environ["GNEWS_API_KEY"]

# Múltiples búsquedas para aumentar resultados
queries = [
    "energy market Latin America",
    "electricity gas Colombia Mexico",
    "energia electrica latinoamerica"
]

articulos = []
for query in queries:
    url = f"https://gnews.io/api/v4/search?q={query}&max=3&apikey={GNEWS_API_KEY}"
    r = requests.get(url)
    data = r.json()
    print(f"Query '{query}': {data.get('totalArticles')} resultados")
    articulos += data.get("articles", [])
    if len(articulos) >= 5:
        break

articulos = articulos[:5]

if not articulos:
    mensaje = "⚠️ No se encontraron noticias hoy sobre energía en los mercados de la región."
    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(telegram_url, data={"chat_id": TELEGRAM_CHAT_ID, "text": mensaje})
    exit()

contexto = ""
links = []
for i, art in enumerate(articulos, 1):
    titulo = art.get("title") or ""
    fuente = art.get("source", {}).get("name") or ""
    descripcion = art.get("description") or ""
    url = art.get("url") or ""
    contexto += f"\nNoticia {i}:\nTítulo: {titulo}\nFuente: {fuente}\nDescripción: {descripcion}\nURL: {url}\n"
    links.append(f"🔗 {titulo}\n{url}")

prompt = f"""Eres un analista experto en mercados de energía eléctrica y gas natural en Latinoamérica.
Analiza estas noticias y explica su impacto en los mercados regulados y no regulados de Colombia, Guatemala, Panamá, México y Ecuador.
Si las noticias están en inglés, tradúcelas primero.

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
