import os
import random
import httpx
import asyncio
import threading
from datetime import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes,
    filters
)

# --- Переменные окружения ---
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Твои цели
goals_text = """\
Улучшать девопс
Жить по графику
Выучить английский
Заниматься спортом
Читать книгу
Слушать музыку
Уметь отдыхать
Жить спокойно и размеренно
Богатство и доброта — это нормально
Будь собой, говори честно, иди своим путём
Перестать страдать, радоваться мелочам и ценить жизнь
Не ленись, слушай близких
Радуйся моменту
Убери социальные сети
Не будь токсичным, знай границы
Развивай речь и дикцию
Мозг любит иллюзии — но ты выбираешь путь
Мой девиз — постоянное развитие и стабильность
"""
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
    "✅ Отжимания (15 мин +1 раз каждый тренировочный день)",
    "✅ Английский (Смотреть ролики на англ)",
    "✅ 1 задача по девопсу каждый рабочий день",
    "✅ 15 минут книги перед сном",
    "✅ Создавать атмосферу добра",
    "✅ Радость + тишина"
    "Отжимания (15 мин +1 раз каждый тренировочный день)",
    "Английский (Смотреть ролики на англ)",
    "1 задача по девопсу каждый рабочий день",
    "15 минут книги перед сном",
    "Создавать атмосферу добра",
    "Радость + тишина"
]

affirmations = [line.strip() for line in goals_text.strip().split('\n') if line.strip()]
affirmations = [line for line in goals_text.strip().split('\n') if line]

# --- Клавиатуры ---
start_keyboard = ReplyKeyboardMarkup([
    ["Start"]
], resize_keyboard=True)
# Клавиатуры
start_keyboard = ReplyKeyboardMarkup(
    [["Start"]], resize_keyboard=True
)

main_keyboard = ReplyKeyboardMarkup([
    ["Today"],
    ["Motivation", "Goals"],
    ["Joke \ud83d\ude08"]
], resize_keyboard=True)
main_keyboard = ReplyKeyboardMarkup(
    [["Today"], ["Motivation", "Goals"], ["Joke"]], resize_keyboard=True
)

# --- Активные пользователи ---
# Хранилище активных пользователей
active_users = set()

# --- Запрос шутки ---
async def fetch_dark_joke():
    async with httpx.AsyncClient() as client:
        try:
            r = await client.get("https://v2.jokeapi.dev/joke/Dark?type=single")
            data = r.json()
            return data.get("joke", "No joke today!")
        except:
            return "Joke fetch failed."
# HTTP сервер для Render
class DummyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'OK')

def run_fake_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("", port), DummyHandler)
    print(f"Fake HTTP server zapushen na portu {port}")
    server.serve_forever()

threading.Thread(target=run_fake_server, daemon=True).start()

# Команды
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    active_users.add(user_id)
    await update.message.reply_text(
        "Welcome! Choose an action below:", reply_markup=main_keyboard
    )

# --- Обработка текстов ---
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text

    if user_id not in active_users:
        if text == "Start":
            active_users.add(user_id)
            await update.message.reply_text("Welcome! Choose an action below:", reply_markup=main_keyboard)
            await update.message.reply_text(
                "Welcome! Choose an action below:", reply_markup=main_keyboard
            )
        else:
            await update.message.reply_text("Press 'Start' to begin 👇", reply_markup=start_keyboard)
            await update.message.reply_text("Press 'Start' to begin", reply_markup=start_keyboard)
        return

    if text == "Today":
        tasks = "\n".join(daily_checklist)
        await update.message.reply_text(f"\ud83d\udcdc Today's checklist:\n{tasks}")
        await update.message.reply_text(f"Today's checklist:\n{tasks}")

    elif text == "Motivation":
        quote = random.choice(affirmations)
        await update.message.reply_text(f"\ud83c\udf1f Motivation:\n{quote}")
        await update.message.reply_text(f"Motivation:\n{quote}")

    elif text == "Goals":
        await update.message.reply_text(goals_text)

    elif text == "Joke \ud83d\ude08":
        joke = await fetch_dark_joke()
    elif text == "Joke":
        joke = await fetch_joke()
        msg = await update.message.reply_text(joke)
        await asyncio.sleep(300)
        try:
@@ -102,25 +116,23 @@
            pass

    else:
        await update.message.reply_text("Unknown command. Choose from the menu ⬆️")

# --- HTTP для Render ---
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

# --- Запуск ---
        await update.message.reply_text("Unknown command. Use the menu.")

# Генерация шуток
async def fetch_joke():
    url = "https://v2.jokeapi.dev/joke/Dark?format=txt"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)Add commentMore actions
            return response.text.strip()
    except:
        return "Couldn't fetch joke."

# Запуск бота
if __name__ == '__main__':
    threading.Thread(target=run_fake_server, daemon=True).start()
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    app.run_polling()
