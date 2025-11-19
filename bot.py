# bot.py
import requests
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, JobQueue

# TOKEN de tu bot
TOKEN = "TU_TOKEN_AQUI"

# Variable global para guardar el precio
precio_actual = None

# Función para actualizar el precio desde Binance
async def actualizar_precio(context: ContextTypes.DEFAULT_TYPE):
    global precio_actual
    try:
        response = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT")
        data = response.json()
        precio_actual = float(data["price"])
        print(f"Precio actualizado: {precio_actual:.2f}")
    except Exception as e:
        print(f"Error al obtener precio: {e}")

# Comando /precio
async def precio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global precio_actual
    if precio_actual is None:
        await update.message.reply_text("Precio aún no disponible. Espera unos segundos...")
    else:
        await update.message.reply_text(f"Tasa Binance (USDT): {precio_actual:.2f}")

# Función principal
async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Handler para /precio
    app.add_handler(CommandHandler("precio", precio))

    # Crear JobQueue y programar actualización cada 5 minutos
    job_queue: JobQueue = app.job_queue
    job_queue.run_repeating(actualizar_precio, interval=300, first=0)  # 300s = 5 minutos

    print("Bot iniciado...")
    await app.run_polling()

# Ejecutar el bot
if __name__ == "__main__":
    asyncio.run(main())
