import os
import random
from datetime import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, JobQueue
import httpx  # для команды /joke

BOT_TOKEN = os.getenv("BOT_TOKEN")

# Основной текст и данные
goals_text = (
    "Улучшать девопс\n"
    "Жить по графику\n"
    "Выучить английский\n"
    "Заниматься спортом\n"
    "Читать книгу\n"
    "Слушать музыку\n"
    "Уметь отдыхать\n"
    "Жить спокойно и размеренно\n"
    "Богатство и доброта - это нормально\n"
    "Будь собой, говори честно, иди своим путём\n"
    "Перестать страдать, нужно радоваться мелочам и ценить жизнь\n"
    "Не ленись, слушай близких\n"
    "Радуйся моменту, цени жизнь\n"
    "Убери социальные сети\n"
    "Не будь токсичным, знай границы\n"
    "Развивай речь и дикцию\n"
    "Мозг любит иллюзии — но ты выбираешь путь\n"
    "Мой девиз - постоянное развитие и стабильность"
)

daily_checklist = [
    "Отжимания (15 мин +1 раз каждый тренировочный день)",
    "Английский (Смотреть ролики на англ)",
    "1 задача по девопсу каждый рабочий день",
    "15 минут книги перед сном",
    "Создавать атмосферу добра",
    "Радость + тишина"
]

affirmations = [line for line in goals_text.strip().split('\n') if line]

# --- Команды ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет, друг! Добро пожаловать!")

async def goals(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(goals_text)

async def daily(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📝 Твои задачи на сегодня:\n" + "\n".join(daily_checklist))

async def affirmation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎯 Мотивация дня:\n" + random.choice(affirmations))

async def joke(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = "https://v2.jokeapi.dev/joke/Dark?format=txt"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=5.0)
            await update.message.reply_text("🃏 Шутка:\n" + response.text.strip())
    except Exception:
        await update.message.reply_text("😅 Не удалось получить шутку. Попробуй позже.")

# --- Напоминания ---
async def morning_reminder(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=context.job.chat_id, text="🌅 Доброе утро, Адиль! Сегодня твои цели ждут: /daily")

async def evening_reflection(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=context.job.chat_id, text="🌙 Вечер! Подумай: что получилось сегодня? Что бы улучшил завтра?")

# --- HTTP-сервер для Render ---
class DummyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

def run_dummy_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("", port), DummyHandler)
    print(f"🌐 Dummy HTTP-сервер запущен на порту {port}")
    server.serve_forever()

# --- Запуск ---
if __name__ == '__main__':
    Thread(target=run_dummy_server, daemon=True).start()

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("goals", goals))
    app.add_handler(CommandHandler("daily", daily))
    app.add_handler(CommandHandler("affirmation", affirmation))
    app.add_handler(CommandHandler("joke", joke))

    job_queue: JobQueue = app.job_queue
    job_queue.run_daily(morning_reminder, time=time(hour=5, minute=0), chat_id=430893419)     # 08:00 по Алматы
    job_queue.run_daily(evening_reflection, time=time(hour=14, minute=30), chat_id=430893419) # 21:30 по Алматы

    app.run_polling()
