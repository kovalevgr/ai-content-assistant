from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from app.db.crud import save_article_history
from app.bots.telegram.state import user_states, user_temp_data

async def handle_article_decision(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    data = query.data

    if user_states.get(user_id) != "awaiting_decision":
        await query.edit_message_text(
            "⚠️ Unexpected action. Please start again with /custom_topic or /top_news."
        )
        return

    if data == "approve_article":
        temp_data = user_temp_data.pop(user_id, None)

        if not temp_data:
            await query.edit_message_text(
                "⚠️ Could not find article data. Please try again."
            )
            user_states.pop(user_id, None)
            return

        # Save article to database
        save_article_history(
            user_id=user_id,
            topic=temp_data["topic"],
            style=temp_data["style"],
            result=temp_data["rewritten_summary"]
        )

        # Prepare publish/cancel buttons
        buttons = [
            [
                InlineKeyboardButton("🚀 Publish Now", callback_data="publish_now"),
                InlineKeyboardButton("❌ Cancel Publish", callback_data="cancel_publish"),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(buttons)

        await query.edit_message_text(
            text="✅ Article approved and saved! 🚀 Would you like to publish it now or cancel?",
            reply_markup=reply_markup
        )

        # Update state and temp data
        user_states[user_id] = "awaiting_publish"
        user_temp_data[user_id] = {
            "topic": temp_data["topic"],
            "style": temp_data["style"],
            "rewritten_summary": temp_data["rewritten_summary"]
        }

    elif data == "edit_article":
        await query.edit_message_text("✏️ Please send the corrected text. I will update it!")
        user_states[user_id] = "awaiting_correction"

    elif data == "cancel_article":
        await query.edit_message_text("❌ Article editing canceled.")
        user_states.pop(user_id, None)
        user_temp_data.pop(user_id, None)

    else:
        await query.edit_message_text("⚠️ Unknown action. Please start again with /custom_topic.")
        user_states.pop(user_id, None)