from telegram import Update
from telegram.ext import ContextTypes

from app.bots.telegram.state import user_states


async def custom_topic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📝 Please type the topic you are interested in:")
    user_states[update.effective_user.id] = "awaiting_topic"