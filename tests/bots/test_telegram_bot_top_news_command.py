import pytest
from unittest.mock import AsyncMock, patch
from telegram import Update
import app.bots.telegram_bot as telegram_bot

class DummyUser:
    def __init__(self, user_id=123456):
        self.id = user_id

class DummyMessage:
    def __init__(self):
        self.sent_texts = []
        self.from_user = DummyUser()

    async def reply_text(self, text, **kwargs):
        self.sent_texts.append(text)

@pytest.mark.asyncio
@patch('app.bots.telegram_bot.fetch_rss_articles')
async def test_top_news_with_articles(mock_fetch_rss_articles):
    # Mock list of found articles
    mock_fetch_rss_articles.return_value = [
        {"title": "Breaking AI News", "link": "http://example.com/article1"},
        {"title": "Tech Trends", "link": "http://example.com/article2"},
    ]

    dummy_message = DummyMessage()
    dummy_update = Update(update_id=7890, message=dummy_message)
    dummy_context = AsyncMock()

    # Call /top_news handler
    await telegram_bot.top_news(dummy_update, dummy_context)

    # Assert
    sent_text = dummy_message.sent_texts[-1]
    assert "breaking ai news" in sent_text.lower()
    assert "tech trends" in sent_text.lower()
    assert "example.com/article1" in sent_text
    assert "example.com/article2" in sent_text

@pytest.mark.asyncio
@patch('app.bots.telegram_bot.fetch_rss_articles')  # 👈 замість search_articles_by_topic
async def test_top_news_without_articles(mock_fetch_rss_articles):
    # Mock no articles found
    mock_fetch_rss_articles.return_value = []

    dummy_message = DummyMessage()
    dummy_update = Update(update_id=7891, message=dummy_message)
    dummy_context = AsyncMock()

    # Call /top_news handler
    await telegram_bot.top_news(dummy_update, dummy_context)

    # Assert that the bot informs no top news available
    sent_text = dummy_message.sent_texts[-1].lower()
    assert "no top news" in sent_text or "no news found" in sent_text