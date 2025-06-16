import os
import random
import httpx
import threading
from datetime import time
from http.server import BaseHTTPRequestHandler, HTTPServer

from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, JobQueue

BOT_TOKEN = os.getenv("BOT_TOKEN")

# Твои цели
goals_text = """\
Улучшать девопс
Делать проект (игру)
Выучить английский
Заниматься спортом
Читать книгу
Слушать музыку
Смотреть ролики в ютубе (без вины)
Жить спокойно, не дрочить
Богатство и доброта — это нормально
Будь собой, говори честно, иди своим путём
Перестань быть "слабым ребёнком", ты взрослый
Не ленись, слушай близких
Радуйся моменту, цени жизнь
Удали Instagram, не сливай фокус
Не будь токсичным, знай границы
Развивай речь и дикцию
Мозг любит иллюзии — но ты выбираешь путь
Мой девиз — постоянное развитие и стабильность
"""

daily_checklist = [
    "✅ Отжимания (15 мин +1 раз каждый тренировочный день)",
    "✅ Английский (Смотреть ролики на англ)",
    "✅ 1 задача по девопсу каждый рабочий день",
    "✅ 15 минут книги перед сном",
    "✅ Создавать атмосферу добра",
    "✅ Радость + тишина"
]

affirmations = goals_text.strip().splitlines()

# Клавиатура
main_keyboard = ReplyKeyboardMarkup(
    [
        ["Сегодня", "Мотивация"],
        ["Цели", "Joke 😈"]
    ],
    resize_keyboard=True
)

# Команды
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет, друг! Я бот-наставник.\nВыбирай, что хочешь сделать:", reply_markup=main_keyboard)

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "Сегодня":
        tasks = "\n".join(daily_checklist)
        await update.message.reply_text(f"📝 Задачи на сегодня:\n{tasks}")
    elif text == "Мотивация":
        quote = random.choice(affirmations)
        await update.message.reply_text(f"🎯 Мотивация дня:\n{quote}")
    elif text == "Цели":
        await update.message.reply_text(goals_text)
    elif text == "Joke 😈":
        joke = await fetch_dark_joke()
        await update.message.reply_text(joke)
    else:
        await update.message.reply_text("Не понял, выбери действие с кнопок ⬆️")

# Шутки с чёрным юмором
async def fetch_dark_joke():
    url = "https://v2.jokeapi.dev/joke/Dark?type=twopart"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            data = response.json()
            return f"😈 {data['setup']}\n👉 {data['delivery']}"
    except Exception:
        return "Не удалось получить шутку. Попробуй позже."

# Напоминания (если используешь chat_id)
async def morning_reminder(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=context.job.chat_id, text="🌅 Доброе утро! Не забудь: /start → Сегодня")

async def evening_reflection(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=context.job.chat_id, text="🌙 Вечер! Подумай: что удалось и что улучшить.")

# Фейковый HTTP-сервер для Render
class DummyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'OK')

def run_fake_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("", port), DummyHandler)
    print(f"Fake HTTP server running on port {port}")
    server.serve_forever()

threading.Thread(target=run_fake_server, daemon=True).start()

# ---------- ЗАПУСК ----------
if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    job_queue: JobQueue = app.job_queue

    # ✅ Замени chat_id на свой (временно можешь распечатать через update.effective_chat.id)
    job_queue.run_daily(morning_reminder, time=time(hour=5, minute=0), chat_id=430893419)     # 08:00 Алматы
    job_queue.run_daily(evening_reflection, time=time(hour=14, minute=30), chat_id=430893419) # 21:30 Алматы

    app.run_polling()
