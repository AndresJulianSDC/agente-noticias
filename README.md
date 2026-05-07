# 📰 Agente de Noticias Energéticas

Bot automático que envía cada mañana a las 7AM (hora Colombia) un resumen de noticias energéticas de Colombia, Guatemala, Panamá, México y Ecuador directamente a Telegram.

## ¿Qué hace?
- Busca noticias reales de las últimas 72 horas sobre energía eléctrica y gas natural
- Analiza el impacto en mercados regulados y no regulados
- Filtra noticias irrelevantes automáticamente
- Envía el análisis con links verificables a Telegram

## 🛠️ Herramientas necesarias (todas gratuitas)
- Cuenta de GitHub
- Cuenta de Telegram
- API Key de Groq: console.groq.com
- API Key de GNews: gnews.io

---

## 📋 Paso a paso

### 1. Hacer fork del repositorio
- Entra al repositorio original
- Clic en Fork arriba a la derecha
- Clic en Create fork

### 2. Crear tu bot de Telegram
1. Abre Telegram y busca @BotFather
2. Escríbele /newbot
3. Elige nombre y username (debe terminar en bot)
4. Guarda el token que te da BotFather
5. Busca tu bot en Telegram y dale Start
6. Entra a este link reemplazando TU_TOKEN: https://api.telegram.org/botTU_TOKEN/getUpdates
7. Guarda el número que aparece en "id" dentro de "chat" — ese es tu Chat ID

### 3. Crear API Key de Groq
1. Ve a console.groq.com
2. Crea cuenta gratuita
3. Ve a API Keys y crea una nueva
4. Copia y guarda tu clave

### 4. Crear API Key de GNews
1. Ve a gnews.io
2. Crea cuenta gratuita
3. Copia tu API Key del dashboard

### 5. Configurar Secrets en GitHub
En tu fork del repositorio ve a Settings → Secrets and variables → Actions → New repository secret y agrega estos 4:

- TELEGRAM_TOKEN — tu token de BotFather
- TELEGRAM_CHAT_ID — tu Chat ID
- GROQ_API_KEY — tu clave de Groq
- GNEWS_API_KEY — tu clave de GNews

### 6. Probar manualmente
1. Ve a la pestaña Actions en tu repositorio
2. Clic en Agente de Noticias Diario
3. Clic en Run workflow
4. Espera 30-60 segundos y revisa tu Telegram

---

## ⏰ Cambiar la hora de envío
Edita el archivo .github/workflows/noticias.yml y cambia el cron:

- 6:00 AM Colombia → 0 11 * * *
- 7:00 AM Colombia → 0 12 * * *
- 8:00 AM Colombia → 0 13 * * *
- 9:00 AM Colombia → 0 14 * * *

---

## ⚠️ Notas importantes
- Las noticias son reales y verificables — siempre revisa los links antes de compartir con superiores
- El bot cubre Colombia, Panamá, México y Ecuador consistentemente. Guatemala tiene cobertura limitada en medios digitales
- El análisis lo genera IA basándose en noticias reales — úsalo como punto de partida, no como fuente definitiva
