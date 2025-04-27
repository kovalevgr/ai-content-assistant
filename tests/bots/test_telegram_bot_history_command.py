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

class DummyDatetime:
    def __init__(self, date_str):
        self.date_str = date_str

    def strftime(self, _):
        return self.date_str

@pytest.mark.asyncio
@patch('app.bots.telegram_bot.get_user_history')
async def test_history_with_records(mock_get_user_history):
    # Mock user history with two articles
    mock_get_user_history.return_value = [
        type('obj', (object,), {
            'topic': 'AI Innovations',
            'style': 'professional',
            'created_at': DummyDatetime('2024-04-27')
        })(),
        type('obj', (object,), {
            'topic': 'Blockchain',
            'style': 'casual',
            'created_at': DummyDatetime('2024-04-26')
        })()
    ]

    dummy_message = DummyMessage()
    dummy_update = Update(update_id=1234, message=dummy_message)
    dummy_context = AsyncMock()

    # Call /history handler
    await telegram_bot.history(dummy_update, dummy_context)

    # Assert that response includes article titles
    assert "Your recent articles" in dummy_message.sent_texts[-1]
    assert "AI Innovations" in dummy_message.sent_texts[-1]
    assert "Blockchain" in dummy_message.sent_texts[-1]

@pytest.mark.asyncio
@patch('app.bots.telegram_bot.get_user_history')
async def test_history_without_records(mock_get_user_history):
    # Mock empty history for user
    mock_get_user_history.return_value = []

    dummy_message = DummyMessage()
    dummy_update = Update(update_id=5678, message=dummy_message)
    dummy_context = AsyncMock()

    # Call /history handler
    await telegram_bot.history(dummy_update, dummy_context)

    # Assert that the bot informs no history is found
    assert "No history found yet" in dummy_message.sent_texts[-1]