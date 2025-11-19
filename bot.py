import asyncio
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

average_price_global = None

async def actualizar_precio():
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
        average_price_global = round(sum(prices)/len(prices), 2)
        print(f"💹 Precio actualizado: {average_price_global} VES")
    except Exception as e:
        print(f"⚠️ Error al actualizar precio: {e}")

async def precio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global average_price_global
    if average_price_global is None:
        await update.message.reply_text("⏳ Precio aún no disponible, intenta de nuevo en unos segundos.")
        return
    formatted_price = f"{average_price_global:,.2f}".replace(",", "'")
    message = f"💹 <b>Tasa Binance (USDT)</b>\n📊 Promedio P2P Venezuela\n\n💰 Precio: <b>{formatted_price} VES</b>\n🔄 Actualizado cada 5 minutos"
    await update.message.reply_text(message, parse_mode="HTML")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Bot activo.\nUsa /precio para ver la tasa Binance actual.")

token = os.getenv("BOT_TOKEN")
app = ApplicationBuilder().token(token).build()

# Handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("precio", precio))

# Función para correr el job cada 5 minutos
async def job_runner(app):
    while True:
        await actualizar_precio()
        await asyncio.sleep(300)  # 5 minutos

# Iniciamos el job paralelo al iniciar la app
async def main():
    asyncio.create_task(job_runner(app))
    await app.run_polling()

# Ejecutamos
asyncio.run(main())
