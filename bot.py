import os
import random
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram.ext import JobQueue

BOT_TOKEN = os.getenv("BOT_TOKEN")

# ---------- ТВОИ ДАННЫЕ ----------
goals_text = """
1. Улучшать девопс
2. Делать проект (игру)
3. Выучить английский
4. Заниматься спортом
5. Читать книгу
6. Слушать музыку
7. Смотреть ролики в ютубе, которые нравятся 
8. Жить спокойно
9. Богатство и доброта — это нормально
10. Будь собой, говори честно, иди своим путём
11. Перестань быть "слабым ребёнком", ты взрослый
12. Не ленись, слушай близких
13. Радуйся моменту, цени жизнь
14. Убери социальные сети
15. Не будь токсичным, знай границы
16. Развивай речь и дикцию
17. Мозг любит иллюзии — но ты выбираешь путь
18. Я счастлив, когда развиваюсь и живу стабильно

"""
daily_checklist = [
    "✅ Спорт (15-30 мин)",
    "✅ Английский (Duolingo / 10 слов)",
    "✅ 1 задача по девопсу",
    "✅ 15 минут книги",
    "✅ Создание игры / проект",
    "✅ Радость + тишина"
]

affirmations = [line.strip() for line in goals_text.strip().split('\n') if line.strip()]

# ---------- КОМАНДЫ ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет, Адиль! Я твой бот-наставник 🙌 Напиши /daily, /goals или /affirmation.")

async def goals(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(goals_text)

async def daily(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tasks = "\n".join(daily_checklist)
    await update.message.reply_text(f"Твои задачи на сегодня:\n{tasks}")

async def affirmation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    quote = random.choice(affirmations)
    await update.message.reply_text(f"🎯 Мотивация:\n{quote}")

# ---------- НАПОМИНАНИЯ ----------
async def morning_reminder(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=context.job.chat_id, text="🌅 Доброе утро, Адиль! Сегодня твои цели ждут: /daily")

async def evening_reflection(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=context.job.chat_id, text="🌙 Вечер! Подумай: что получилось сегодня? Что бы улучшил завтра?")

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
    app.add_handler(CommandHandler("goals", goals))
    app.add_handler(CommandHandler("daily", daily))
    app.add_handler(CommandHandler("affirmation", affirmation))

    job_queue: JobQueue = app.job_queue

    # Добавляем напоминания (по серверному времени UTC!)
    job_queue.run_daily(morning_reminder, time=time(hour=5, minute=0), chat_id=YOUR_CHAT_ID)     # 08:00 по Алматы
    job_queue.run_daily(evening_reflection, time=time(hour=14, minute=30), chat_id=YOUR_CHAT_ID) # 21:30 по Алматы

    app.run_polling()
