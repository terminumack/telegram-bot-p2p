import os
import asyncio
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

# Obtener el token desde la variable de entorno
TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise ValueError("No se encontró el token. Asegúrate de definir la variable de entorno 'TOKEN' en Railway.")

# Función de inicio / comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("¡Hola! Soy tu bot funcionando en Railway 🚀")

# Tarea periódica (ejemplo)
async def periodic_task(context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = os.getenv("CHAT_ID")  # Opcional: definir un chat específico
    if chat_id:
        await context.bot.send_message(chat_id=chat_id, text="Mensaje periódico desde el bot.")

async def main():
    # Crear la aplicación con el token
    app = ApplicationBuilder().token(TOKEN).build()

    # Comandos
    app.add_handler(CommandHandler("start", start))

    # JobQueue para tareas periódicas
    app.job_queue.run_repeating(periodic_task, interval=300, first=10)  # cada 5 minutos

    # Inicializar y correr el bot
    await app.initialize()
    await app.start()
    print("Bot corriendo en Railway...")
    await app.updater.start_polling()  # Mantener el bot corriendo
    await app.idle()  # Esperar a que se detenga el bot

if __n
