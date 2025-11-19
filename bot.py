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
    price = data["data"][0]["adv"]["price"]

    await update.message.reply_text(f"💵 Precio USDT (BUY): {price} VES")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot activo. Usa /precio para ver el precio.")

token = os.getenv("BOT_TOKEN")

app = ApplicationBuilder().token(token).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("precio", precio))

app.run_polling()
