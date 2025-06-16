from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")

goals_text = """
1. Улучшать девопс
2. Делать проект (игру)
3. Выучить английский
...
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет, Адиль! Я бот-наставник 💪")

async def goals(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(goals_text)

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("goals", goals))
    app.run_polling()
