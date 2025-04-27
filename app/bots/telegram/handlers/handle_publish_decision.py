from telegram import Update
from telegram.ext import ContextTypes
from app.bots.telegram.state import user_states, user_temp_data

async def handle_publish_decision(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    data = query.data

    if user_states.get(user_id) != "awaiting_publish":
        await query.edit_message_text(
            "⚠️ Unexpected action. Please start again with /custom_topic or /top_news."
        )
        return

    if data == "publish_now":
        temp_data = user_temp_data.pop(user_id, None)

        if not temp_data:
            await query.edit_message_text(
                "⚠️ Could not find article data. Please try again."
            )
            user_states.pop(user_id, None)
            return

        # Here you would add real publishing logic (e.g., post to blog, Medium, Telegram channel, etc.)
        await query.edit_message_text(
            f"🎉 Your article '*{temp_data['topic']}*' has been successfully published!",
            parse_mode="Markdown"
        )

        user_states.pop(user_id, None)

    elif data == "cancel_publish":
        # User canceled publishing
        user_states.pop(user_id, None)
        user_temp_data.pop(user_id, None)

        await query.edit_message_text(
            "❌ Publishing canceled. Your article is safely stored in history."
        )