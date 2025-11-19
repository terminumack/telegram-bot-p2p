import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, JobQueue
import os

# Variable global para almacenar el precio
average_price_global = None

async def actualizar_precio(context: ContextTypes.DEFAULT_TYPE):
    global average_price_global
    url = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"
    payload = {
        "page": 1,
        "rows": 10,
        "payTypes": [],
        "asset": "USDT",
        "fiat": "VES",
        "tradeType": "BUY"
    }
    headers = {"Content-Type": "application/json"}
    try:
        r = requests.post(url, json=payload, headers=headers, timeout=10)
        data = r.json()
        prices = [float(item["adv"]["price"]) for item in data["data"]]
        average_price_global = round(sum(prices) / len(prices), 2)
        print(f"💹 Precio actualizado: {average_price_global} VES")
    except Exception as e:
        print(f"⚠️ Error al actualizar precio: {e}")

async def precio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global average_price_global
    if average_price_global is None:
        await update.message.reply_text("⏳ Precio aún no disponible, intenta de nuevo en unos segundos.")
        return

    # Formato de miles con 2 decimales
    formatted_price = f"{average_price_global:,.2f}".replace(",", "'")

    # Mensaje profesional
    message = (
        f"💹 <b>Tasa Binance (USDT)</b>\n"
        f"📊 Promedio P2P Venezuela\n\n"
        f"💰 Precio: <b>{formatted_price} VES</b>\n"
        f"🔄 Actualizado cada 5 minutos"
    )
    await update.message.reply_text(message, parse_mode='HTML')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Bot activo.\nUsa /precio para ver la tasa Binance actual."
    )

# TOKEN del bot desde variables de entorno
token = os.getenv("BOT_TOKEN")

# Configuración del bot
app = ApplicationBuilder().token(token).build()

# Agregar handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("precio", precio))

# Configurar job queue para actualizar cada 5 minutos
job_queue = app.job_queue
job_queue.run_repeating(actualizar_precio, interval=300, first=0)  # 300s = 5 minutos

# Ejecutar el bot
app.run_polling()
