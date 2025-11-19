import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, Job
import os

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
    formatted_price = f"{average_price_global:,.2f}".replace(",", "'")
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

token = os.getenv("BOT_TOKEN")

# Creamos la aplicación
app = ApplicationBuilder().token(token).build()

# Handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("precio", precio))

# Agregamos job de actualización cada 5 minutos usando post_init
async def post_init(application):
    application.job_queue.run_repeating(actualizar_precio, interval=300, first=0)

app.post_init = post_init

# Ejecutamos el bot
app.run_polling()
