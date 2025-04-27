import pytest
from unittest.mock import AsyncMock, patch
from telegram import Update
import app.bots.telegram_bot as telegram_bot

class DummyUser:
    def __init__(self, user_id=123456):
        self.id = user_id

class DummyMessage:
    def __init__(self):
        self.text = None
        self.sent_texts = []
        self.from_user = DummyUser()

    async def reply_text(self, text, **kwargs):
        self.text = text
        self.sent_texts.append(text)
        return self

class DummyContext:
    bot = None
    args = []
    kwargs = {}

@pytest.mark.asyncio
@patch('app.bots.telegram_bot.save_article_history')
@patch('app.bots.telegram_bot.search_articles_by_topic')
@patch('app.bots.telegram_bot.summarize_articles')
@patch('app.bots.telegram_bot.rewrite_text')
async def test_custom_topic_flow(mock_rewrite_text, mock_summarize_articles, mock_search_articles, mock_save_history):
    # Mock search_articles
    mock_search_articles.return_value = [
        {"title": "AI Innovations", "summary": "Changing the world.", "link": "http://example.com/ai-news"}
    ]

    # Mock summarize_articles
    mock_summarize_articles.return_value = "Summarized text about AI."

    # Mock rewrite_text
    mock_rewrite_text.return_value = "Rewritten casual text about AI."

    # Dummy Telegram objects
    dummy_message = DummyMessage()
    dummy_update = Update(update_id=1234, message=dummy_message)
    dummy_context = AsyncMock()

    # Step 1: User sends /custom_topic
    await telegram_bot.custom_topic(dummy_update, dummy_context)
    assert "Please type the topic" in dummy_message.sent_texts[-1]

    # Step 2: User enters topic
    dummy_message.sent_texts = []
    dummy_update.message.text = "AI innovations"

    await telegram_bot.handle_message(dummy_update, dummy_context)
    assert "choose a writing style" in dummy_message.sent_texts[-1]

    # Step 3: User selects style
    dummy_message.sent_texts = []
    dummy_update.message.text = "casual"

    await telegram_bot.handle_message(dummy_update, dummy_context)

    # Verify that rewritten text was sent
    assert "Rewritten casual text" in dummy_message.sent_texts[-1]
    assert "casual" in dummy_message.sent_texts[-1].lower()

    # Verify that history was saved
    mock_save_history.assert_called_once()

    # Verify states are cleaned
    assert dummy_update.effective_user.id not in telegram_bot.user_states
    assert dummy_update.effective_user.id not in telegram_bot.user_temp_data