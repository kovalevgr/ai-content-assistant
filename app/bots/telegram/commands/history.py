from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from app.db.crud import get_user_history

async def history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    # Get full user history
    records = get_user_history(user_id)

    if not records:
        await update.message.reply_text("📭 No history found yet.")
        return

    # Build topics from history
    keyboard = [
        [InlineKeyboardButton(record.topic, callback_data=f"generate:{record.topic}")]
        for record in records
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "📝 Here are your recent topics. Choose one to generate a new article:",
        reply_markup=reply_markup
    )