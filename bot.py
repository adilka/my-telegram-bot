from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

# Токен из переменных окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Контент
goals_text = """
1. Улучшать девопс
2. Делать игру
3. Учить английский
...
"""

# Команды
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет, Адиль! Я бот-наставник 💪")

async def goals(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(goals_text)

# Фейковый HTTP сервер для Render
class DummyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'OK')

def run_fake_server():
    port = int(os.environ.get("PORT", 10000))  # Render шлёт этот порт
    server = HTTPServer(("", port), DummyHandler)
    print(f"Fake HTTP server запущен на порту {port}")
    server.serve_forever()

# Запуск фейкового сервера в фоне
threading.Thread(target=run_fake_server, daemon=True).start()

# Запуск Telegram-бота
if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("goals", goals))
    app.run_polling()
