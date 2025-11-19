import asyncio
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

import requests

TOKEN = "TU_TOKEN_AQUI"

# ----------------------
# Funciones de comandos
# ----------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot iniciado correctamente!")

# ----------------------
# Tarea periódica
# ----------------------
async def periodic_task(context: ContextTypes.DEFAULT_TYPE):
    # Ejemplo de tarea periódica
    print("Ejecutando tarea periódica...")
    # Aquí puedes poner cualquier código que quieras ejecutar cada X segundos
    # Ejemplo: requests.get("https://api.example.com/endpoint")

# ----------------------
# Función principal
# ----------------------
async def main():
    # Crear la aplicación del bot
    app = ApplicationBuilder().token(TOKEN).build()

    # Comandos
    app.add_handler(CommandHandler("start", start))

    # JobQueue seguro
    if app.job_queue:
        app.job_queue.run_repeating(periodic_task, interval=300, first=10)
    else:
        print("JobQueue no configurada correctamente")

    # Inicializar y arrancar el bot
    await app.initialize()
    await app.start()
    await app.updater.start_polling()  # Para usar polling
    await app.updater.idle()

# ----------------------
# Ejecutar bot
# ----------------------
if __name__ == "__main__":
    asyncio.run(main())
