from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from app.agents.image_generator import generate_images
from app.agents.rewriter import rewrite_text
from app.agents.summarizer import summarize_articles
from app.agents.topic_aggregator import search_articles_by_topic
from app.bots.telegram.state import user_states, user_temp_data


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text

    if user_states.get(user_id) == "awaiting_topic":
        topic = text
        user_states[user_id] = "awaiting_style"

        found_articles = search_articles_by_topic(topic)
        user_temp_data[user_id] = {
            "topic": topic,
            "articles": found_articles
        }

        if not found_articles:
            await update.message.reply_text(
                f"😔 Sorry, no articles found related to *{topic}*.",
                parse_mode="Markdown"
            )
            user_states.pop(user_id, None)
            user_temp_data.pop(user_id, None)
            return

        await update.message.reply_text(
            "🖋️ Please choose a writing style:\n- Professional\n- Casual\n- Emotional\n- Technical",
        )

    elif user_states.get(user_id) == "awaiting_style":
        chosen_style = text.strip().lower()
        valid_styles = ["professional", "casual", "emotional", "technical"]

        if chosen_style not in valid_styles:
            await update.message.reply_text(
                "❌ Invalid style. Please choose one of: Professional, Casual, Emotional, Technical."
            )
            return

        data = user_temp_data.pop(user_id, None)
        if not data:
            await update.message.reply_text("⚠️ Something went wrong. Please try again with /custom_topic.")
            user_states.pop(user_id, None)
            return

        topic = data["topic"]
        articles = data["articles"]

        summary = await summarize_articles(articles)
        images = await generate_images(topic)
        rewritten_summary = await rewrite_text(summary, style=chosen_style, images=images)

        # Save rewritten article temporarily to user_temp_data
        user_temp_data[user_id] = {
            "topic": topic,
            "style": chosen_style,
            "rewritten_summary": rewritten_summary,
        }

        await update.message.reply_text(
            f"📝 Here’s a *{chosen_style.title()}* style article for *{topic}*:\n\n{rewritten_summary}",
            parse_mode="Markdown"
        )

        # Show Approve/Edit buttons
        buttons = [
            [
                InlineKeyboardButton("✅ Approve", callback_data="approve_article"),
                InlineKeyboardButton("✏️ Edit", callback_data="edit_article"),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(buttons)

        await update.message.reply_text(
            "What would you like to do with this article?",
            reply_markup=reply_markup
        )

        # Update user state to awaiting decision
        user_states[user_id] = "awaiting_decision"

    else:
        await update.message.reply_text(
            "❓ Please use /top_news or /custom_topic."
        )