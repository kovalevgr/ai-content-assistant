from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from app.agents.rss_aggregator import fetch_rss_articles

import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привіт! Я твій AI Content Assistant! 🚀\nНапиши /top_news або /custom_topic")


async def top_news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔍 Fetching top news for you...")

    articles = fetch_rss_articles(max_articles=3)

    if not articles:
        await update.message.reply_text("😔 Sorry, no news found.")
        return

    batch_message = ""
    batch_size = 5

    for idx, article in enumerate(articles, start=1):
        batch_message += f"📰 *{article['title']}*\n[Read more]({article['link']})\n\n"

        if idx % batch_size == 0 or idx == len(articles):
            await update.message.reply_text(batch_message.strip(), parse_mode="Markdown")
            batch_message = ""

async def custom_topic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✏️ Введи тему, яка тебе цікавить:")


async def topics(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📚 Ось твої попередні теми (поки ще порожньо)")


def run_bot():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("top_news", top_news))
    app.add_handler(CommandHandler("custom_topic", custom_topic))
    app.add_handler(CommandHandler("topics", topics))

    print("✅ Бот запущено. Чекаю команди...")

    app.run_polling()