from telegram import Update
from telegram.ext import ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привіт! Я твій AI Content Assistant! 🚀\nНапиши /top_news або /custom_topic"
    )