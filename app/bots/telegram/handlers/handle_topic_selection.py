from telegram import Update
from telegram.ext import ContextTypes


async def handle_topic_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Extract the topic from the callback data
    data = query.data
    if data.startswith("generate:"):
        topic = data.split("generate:")[1]

        await query.message.reply_text(f"Generating a new article on *{topic}*...", parse_mode="Markdown")