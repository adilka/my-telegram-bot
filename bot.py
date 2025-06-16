import os
import random
import httpx
import asyncio
import threading
from datetime import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes,
    filters, JobQueue
)

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

# Клавиатуры
main_keyboard = ReplyKeyboardMarkup(
    [["Today"], ["Motivation", "Goals"], ["Joke"]], resize_keyboard=True
)

# HTTP сервер для Render
class DummyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'OK')

def run_fake_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("", port), DummyHandler)
    print(f"Fake HTTP server запущен на порту {port}")
    server.serve_forever()

threading.Thread(target=run_fake_server, daemon=True).start()

# Команды
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Выбирай действие ниже:", reply_markup=main_keyboard
    )

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if text == "Today":
        tasks = "\n".join(daily_checklist)
        await update.message.reply_text(f"Твои задачи на сегодня:\n{tasks}")

    elif text == "Motivation":
        quote = random.choice(affirmations)
        await update.message.reply_text(f"Мотивация дня:\n{quote}")

    elif text == "Goals":
        await update.message.reply_text(goals_text)

    elif text == "Joke":
        joke = await fetch_joke()
        msg = await update.message.reply_text(joke)
        await asyncio.sleep(300)
        try:
            await msg.delete()
        except:
            pass

    else:
        await update.message.reply_text("Выбери действие с кнопок.")

# Генерация шуток
async def fetch_joke():
    url = "https://v2.jokeapi.dev/joke/Dark?format=txt"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            return response.text.strip()
    except:
        return "Не удалось получить шутку."

# Напоминания
async def morning_reminder(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=context.job.chat_id, text="Доброе утро, Адиль! Сегодня твои цели ждут: Today")

async def evening_reflection(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=context.job.chat_id, text="Вечер! Подумай: что получилось сегодня? Что бы улучшил завтра?")

# Запуск бота
if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    job_queue: JobQueue = app.job_queue
    job_queue.run_daily(morning_reminder, time=time(hour=5, minute=0), chat_id=430893419)
    job_queue.run_daily(evening_reflection, time=time(hour=14, minute=30), chat_id=430893419)

    app.run_polling()
