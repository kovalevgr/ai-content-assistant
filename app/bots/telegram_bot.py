from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

from app.agents.topic_aggregator import search_articles_by_topic
from app.agents.rss_aggregator import fetch_rss_articles
from app.agents.summarizer import summarize_articles
from app.agents.rewriter import rewrite_text

import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Simple in-memory user states
user_states = {}
user_temp_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привіт! Я твій AI Content Assistant! 🚀\nНапиши /top_news або /custom_topic")

async def top_news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔍 Fetching top news for you...")

    articles = fetch_rss_articles(max_articles=3)

    if not articles:
        await update.message.reply_text("😔 Sorry, no news found.")
        return

    await _send_articles_batch(update, articles)

async def custom_topic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📝 Please type the topic you are interested in:")
    user_states[update.effective_user.id] = "awaiting_topic"

async def topics(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📚 Ось твої попередні теми (поки ще порожньо)")

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
        rewritten_summary = await rewrite_text(summary, style=chosen_style)

        await update.message.reply_text(
            f"📝 Here’s a *{chosen_style.title()}* style article for *{topic}*:\n\n{rewritten_summary}",
            parse_mode="Markdown"
        )

        user_states.pop(user_id, None)

    else:
        await update.message.reply_text(
            "❓ Please use /top_news or /custom_topic."
        )

async def _send_articles_batch(update, articles: list, batch_size: int = 5):
    batch_message = ""

    for idx, article in enumerate(articles, start=1):
        batch_message += f"📰 *{article['title']}*\n[Read more]({article['link']})\n\n"

        if idx % batch_size == 0 or idx == len(articles):
            await update.message.reply_text(batch_message.strip(), parse_mode="Markdown")
            batch_message = ""

def run_bot():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("top_news", top_news))
    app.add_handler(CommandHandler("custom_topic", custom_topic))
    app.add_handler(CommandHandler("topics", topics))

    # Handlers
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Бот запущено. Чекаю команди...")

    app.run_polling()