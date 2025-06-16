from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, JobQueue
import os
import threading
import random
from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import time

# Токен из переменных окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Контент
goals_text = """
1. Улучшать девопс
2. Делать проект (игру)
3. Выучить английский
4. Заниматься спортом
5. Читать книгу
6. Слушать музыку
7. Смотреть ролики в ютубе (без вины)
8. Жить спокойно, не дрочить
9. Богатство и доброта — это нормально
10. Будь собой, говори честно, иди своим путём
11. Перестань быть "слабым ребёнком", ты взрослый
12. Не ленись, слушай близких
13. Радуйся моменту, цени жизнь
14. Удали Instagram, не сливай фокус
15. Не будь токсичным, знай границы
16. Развивай речь и дикцию
17. Мозг любит иллюзии — но ты выбираешь путь
18. Мой девиз - постоянное развитие и стабильность
"""

daily_checklist = [
    "✅ Спорт (15–30 мин)",
    "✅ Английский (Duolingo / 10 слов)",
    "✅ 1 задача по девопсу",
    "✅ 15 минут книги",
    "✅ Создание игры / проект",
    "✅ Радость + тишина"
]

affirmations = [line.strip() for line in goals_text.strip().split('\n') if line.strip()]

# Клавиатура
main_keyboard = ReplyKeyboardMarkup(
    [
        ["Сегодня", "Мотивация"],
        ["Цели / Установки", "Закрыть"]
    ],
    resize_keyboard=True
)

# ---------- КОМАНДЫ ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет, Адиль! Я твой бот-наставник. Выбирай, что хочешь сделать:",
        reply_markup=main_keyboard
    )

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "Сегодня":
        tasks = "\n".join(daily_checklist)
        await update.message.reply_text(f"📝 Задачи на сегодня:\n{tasks}")
    elif text == "Мотивация":
        quote = random.choice(affirmations)
        await update.message.reply_text(f"🎯 Мотивация дня:\n{quote}")
    elif text == "Цели / Установки":
        await update.message.reply_text(goals_text)
    elif text == "Закрыть":
        await update.message.reply_text("Клавиатура убрана", reply_markup=ReplyKeyboardRemove())
    else:
        await update.message.reply_text("Не понял, выбери действие с кнопок ⬆️")

# ---------- НАПОМИНАНИЯ ----------
async def morning_reminder(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=context.job.chat_id, text="🌅 Доброе утро! Не забудь: /start → Сегодня")

async def evening_reflection(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=context.job.chat_id, text="🌙 Вечер! Подумай: что удалось и что улучшить.")

# ---------- ФЕЙКОВЫЙ HTTP-СЕРВЕР ДЛЯ RENDER ----------
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
