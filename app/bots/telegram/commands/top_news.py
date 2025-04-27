from telegram import Update
from telegram.ext import ContextTypes
from app.agents.rss_aggregator import fetch_rss_articles

async def top_news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔍 Fetching top news for you...")

    articles = fetch_rss_articles(max_articles=3)

    if not articles:
        await update.message.reply_text("😔 Sorry, no news found.")
        return

    await _send_articles_batch(update, articles)

async def _send_articles_batch(update, articles: list, batch_size: int = 5):
    batch_message = ""

    for idx, article in enumerate(articles, start=1):
        batch_message += f"📰 *{article['title']}*\n[Read more]({article['link']})\n\n"

        if idx % batch_size == 0 or idx == len(articles):
            await update.message.reply_text(batch_message.strip(), parse_mode="Markdown")
            batch_message = ""