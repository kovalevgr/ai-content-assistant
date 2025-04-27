import pytest
from unittest.mock import AsyncMock, patch
from telegram import Update
from app.bots.telegram_bot import start, top_news, custom_topic, user_states, handle_message

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
async def test_start():
    dummy_message = DummyMessage()
    dummy_update = Update(update_id=1234, message=dummy_message)
    dummy_context = DummyContext()

    await start(dummy_update, dummy_context)

    assert dummy_message.text.startswith("Привіт! Я твій AI Content Assistant"), \
        f"Очікуваний текст не знайдено. Отримано: {dummy_message.text}"

@pytest.mark.asyncio
@patch('app.bots.telegram_bot.fetch_rss_articles')
async def test_top_news(mock_fetch_articles):
    mock_fetch_articles.return_value = [
        {"title": f"Test Title {i}", "link": f"http://example.com/{i}"} for i in range(1, 11)
    ]

    dummy_message = DummyMessage()
    dummy_update = Update(update_id=1234, message=dummy_message)
    dummy_context = AsyncMock()

    await top_news(dummy_update, dummy_context)

    assert len(dummy_message.sent_texts) == 3

    assert "Test Title 1" in dummy_message.sent_texts[1]
    assert "Test Title 6" in dummy_message.sent_texts[2]

@pytest.mark.asyncio
@patch('app.bots.telegram_bot.search_articles_by_topic')
@patch('app.bots.telegram_bot.summarize_articles')
async def test_custom_topic_flow(mock_summarize_articles, mock_search_articles):
    mock_search_articles.return_value = [
        {"title": "AI Innovations are changing the world", "link": "http://example.com/ai-news"}
    ]

    mock_summarize_articles.return_value = "This is a summarized article about AI innovations."

    dummy_message = DummyMessage()
    dummy_update = Update(update_id=1234, message=dummy_message)
    dummy_context = AsyncMock()

    await custom_topic(dummy_update, dummy_context)

    assert dummy_message.sent_texts[-1] == "📝 Please type the topic you are interested in:"
    assert user_states[dummy_update.effective_user.id] == "awaiting_topic"

    dummy_message.sent_texts = []
    dummy_update.message.text = "AI innovations"

    await handle_message(dummy_update, dummy_context)

    assert "short summary" in dummy_message.sent_texts[-1]
    assert "AI innovations" in dummy_message.sent_texts[-1]

    assert dummy_update.effective_user.id not in user_states