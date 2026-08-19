import os
import requests
import xml.etree.ElementTree as ET
from urllib.parse import quote
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

GROQ_API_KEY = os.environ["GROQ_API_KEY"]
TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

# Un artículo garantizado por país + búsqueda regional
searches = [
    ("gas natural Colombia mercado energía 2026", 2),
    ("energia Colombia XM embalses 2026", 1),
    ("Guatemala CNEE tarifa electrica 2026", 1),
    ("Guatemala AMM energia mayorista 2026", 1),
    ("energia Panama electricidad tarifas 2026", 1),
    ("gas natural Mexico energia inversion 2026", 2),
    ("energia Ecuador electricidad Cenace 2026", 1),
]

articulos = []
ahora = datetime.now(timezone.utc)
vistos = set()

for query, max_por_busqueda in searches:
    url = f"https://news.google.com/rss/search?q={quote(query)}&hl=es&gl=CO&ceid=CO:es"
    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    if r.status_code != 200:
        continue
    root = ET.fromstring(r.content)
    items = root.findall(".//item")
    count = 0
    for item in items:
        if count >= max_por_busqueda:
            break
        titulo = item.findtext("title") or ""
        link = item.findtext("link") or ""
        descripcion = item.findtext("description") or ""
        fuente = item.findtext("source") or "Google News"
        fecha_str = item.findtext("pubDate") or ""
        try:
            fecha = parsedate_to_datetime(fecha_str)
            horas_diff = (ahora - fecha).total_seconds() / 3600
            if horas_diff > 72:
                continue
        except:
            continue
        if titulo in vistos:
            continue
        vistos.add(titulo)
        articulos.append({
            "titulo": titulo,
            "link": link,
            "descripcion": descripcion,
            "fuente": fuente,
            "fecha": fecha_str
        })
        count += 1

if not articulos:
    mensaje = "⚠️ No se encontraron noticias en las últimas 72 horas sobre energía en los mercados de la región."
    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(telegram_url, data={"chat_id": TELEGRAM_CHAT_ID, "text": mensaje})
    exit()

contexto = ""
links = []
for i, art in enumerate(articulos, 1):
    contexto += f"\nNoticia {i}:\nTítulo: {art['titulo']}\nFuente: {art['fuente']}\nFecha: {art['fecha']}\nDescripción: {art['descripcion']}\nURL: {art['link']}\n"
    links.append(f"🔗 {art['titulo']}\n{art['link']}")

prompt = f"""Eres un analista senior experto en mercados de energía eléctrica y gas natural en Latinoamérica.
Tu análisis será leído por profesionales de una multinacional del sector energético.

Analiza estas noticias reales de las últimas 72 horas y explica con precisión técnica su impacto en los mercados regulados y no regulados de Colombia, Guatemala, Panamá, México y Ecuador.
Si alguna noticia no es relevante para estos mercados, indícalo claramente.
No inventes datos. Solo analiza lo que está en las noticias proporcionadas.
Si una noticia es sobre eventos, ferias, conferencias o temas no relacionados directamente con precios, tarifas, suministro o política energética, OMÍTELA completamente del análisis.
IMPORTANTE: NO incluyas en el resumen las noticias que clasificaste como relevancia Baja. Solo incluye noticias de relevancia Alta o Media.
{contexto}

Responde en español con este formato:

📰 RESUMEN ENERGÉTICO DEL DÍA

🔹 Noticia 1:
Título: ...
Fuente: ...
Fecha: ...
Resumen: ...
Impacto mercado regulado: ...
Impacto mercado no regulado: ...
Relevancia para la región: Alta / Media / Baja
¿Qué debes saber?: ...

(repite para cada noticia)

📌 Conclusión estratégica del día: ...

⚠️ Nota: Este análisis se basa en noticias reales de las últimas 72 horas. Verifica los links antes de tomar decisiones."""

groq_url = "https://api.groq.com/openai/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}
body = {
    "model": "openai/gpt-oss-20b",
    "messages": [{"role": "user", "content": prompt}],
    "temperature": 0.3
}

r = requests.post(groq_url, headers=headers, json=body)
data = r.json()
if "choices" not in data:
    raise Exception(f"Error Groq: {data}")
analisis = data["choices"][0]["message"]["content"]

links_texto = "\n\n🔗 FUENTES VERIFICABLES:\n" + "\n\n".join(links)
mensaje_final = analisis + links_texto

def enviar_telegram(texto):
    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(telegram_url, data={"chat_id": TELEGRAM_CHAT_ID, "text": texto})

if len(mensaje_final) <= 4096:
    enviar_telegram(mensaje_final)
else:
    partes = [mensaje_final[i:i+4000] for i in range(0, len(mensaje_final), 4000)]
    for parte in partes:
        enviar_telegram(parte)
