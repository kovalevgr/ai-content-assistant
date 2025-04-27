from telegram import Update
from telegram.ext import ContextTypes

async def topics(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📚 Ось твої попередні теми (поки ще порожньо)")