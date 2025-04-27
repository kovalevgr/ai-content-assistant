import os

from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackQueryHandler

from app.bots.telegram.commands import start, top_news, custom_topic, topics, history
from app.bots.telegram.handlers import handle_message, handle_topic_selection, handle_article_decision, \
    handle_publish_decision

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