import os

from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackQueryHandler

from app.bots.telegram.commands.start import start
from app.bots.telegram.commands.top_news import top_news
from app.bots.telegram.commands.custom_topic import custom_topic
from app.bots.telegram.commands.topics import topics
from app.bots.telegram.commands.history import history

from app.bots.telegram.handlers.handle_message import handle_message
from app.bots.telegram.handlers.handle_topic_selection import handle_topic_selection
from app.bots.telegram.handlers.handle_article_decision import handle_article_decision
from app.bots.telegram.handlers.handle_publish_decision import handle_publish_decision

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

def run_bot():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("top_news", top_news))
    app.add_handler(CommandHandler("custom_topic", custom_topic))
    app.add_handler(CommandHandler("topics", topics))
    app.add_handler(CommandHandler("history", history))

    # Handlers
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(handle_topic_selection, pattern="^generate:"))
    app.add_handler(CallbackQueryHandler(handle_article_decision, pattern="^(approve_article|edit_article)$"))
    app.add_handler(CallbackQueryHandler(handle_publish_decision, pattern="^(publish_now|cancel_publish)$"))

    print("✅ Бот запущено. Чекаю команди...")

    app.run_polling()