import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, JobQueue

# Obtener token desde variables de entorno
TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise ValueError("No se encontró el token. Asegúrate de definir la variable de entorno 'TOKEN' en Railway.")

# Función para /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("¡Hola! Soy tu bot funcionando en Railway 🚀")

# Tarea periódica (cada 5 minutos)
async def periodic_task(context: ContextTypes.DEFAULT_TYPE):
    # Aquí puedes poner lo que quieras que haga tu bot periódicamente
    print("Tarea periódica ejecutada")

async def main():
    # Crear la aplicación
    app = ApplicationBuilder().token(TOKEN).build()

    # Agregar comando /start
    app.add_handler(CommandHandler("start", start))

    # Configurar job queue
    job_queue: JobQueue = app.job_queue
    job_queue.run_repeating(periodic_task, interval=300, first=10)

    # Inicializar y arrancar el bot
    await app.initialize()
    print("Bot inicializado y listo")
    await app.start()
    await app.updater.start_polling()
    await app.idle()

if __name__ == "__main__":
    asyncio.run(main())
# Ejecutar bot
# ----------------------
if __name__ == "__main__":
    asyncio.run(main())
