import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

async def precio(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
    r = requests.post(url, json=payload, headers=headers)
    data = r.json()

    # Calculamos el promedio
    prices = [float(item["adv"]["price"]) for item in data["data"]]
    average_price = sum(prices) / len(prices)

    # Formato de número con separador de miles y 2 decimales
    formatted_price = f"{average_price:,.2f}".replace(",", "'")

    # Mensaje profesional
    message = (
        f"💹 <b>Tasa Binance (USDT)</b>\n"
        f"📊 Promedio P2P Venezuela\n\n"
        f"💰 Precio: <b>{formatted_price} VES</b>\n"
        f"🔄 Actualizado en tiempo real"
    )

    await update.message.reply_text(message, parse_mode='HTML')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Bot activo.\nUsa /precio para ver la tasa Binance actual."
    )

token = os.getenv("BOT_TOKEN")

app = ApplicationBuilder().token(token).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("precio", precio))

app.run_polling()
