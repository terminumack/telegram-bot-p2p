# bot.py
import logging
import asyncio
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    JobQueue,
)

TOKEN = "TU_TOKEN_AQUI"

# Configuración de logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Comando de inicio
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("¡Hola! Soy tu bot funcionando en PTB 20.5.")

# Comando de guardar información
user_data_storage = {}

async def save_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        key = update.message.from_user.id
        user_data_storage[key] = " ".join(context.args)
        await update.message.reply_text(f"Información guardada: {user_data_storage[key]}")
    else:
        await update.message.reply_text("Por favor, envía algo para guardar. Ejemplo: /save Hola")

# Job que se ejecuta cada 5 minutos
async def periodic_task(context: ContextTypes.DEFAULT_TYPE):
    logging.info("Ejecutando tarea periódica")
    # Aquí puedes hacer algo con user_data_storage
    for user_id, info in user_data_storage.items():
        logging.info(f"Usuario {user_id} -> Info: {info}")

async def main():
    # Creamos la aplicación
    app = ApplicationBuilder().token(TOKEN).build()

    # Agregamos comandos
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("save", save_info))

    # Job queue: ejecutar periodic_task cada 5 minutos
    app.job_queue.run_repeating(periodic_task, interval=300, first=10)

    # Ejecutar el bot
    await app.start()
    await app.updater.start_polling()  # Para que funcione en Railway
    await app.updater.idle()

if __name__ == "__main__":
    asyncio.run(main())
