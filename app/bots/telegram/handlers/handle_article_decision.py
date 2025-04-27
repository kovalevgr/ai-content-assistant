from telegram import Update
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

        await query.edit_message_text(
            "✅ Article approved and saved successfully!"
        )
        user_states.pop(user_id, None)

    elif data == "edit_article":
        user_states[user_id] = "awaiting_correction"

        await query.edit_message_text(
            "✏️ Please send the corrected text. I will update it!"
        )

    else:
        await query.edit_message_text(
            "❓ Unknown action."
        )