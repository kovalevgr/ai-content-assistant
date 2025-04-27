import pytest
from unittest.mock import AsyncMock, patch
from telegram import Update

from app.bots.telegram.commands.history import history

class DummyUser:
    def __init__(self, user_id=123456):
        self.id = user_id

class DummyMessage:
    def __init__(self):
        self.sent_texts = []
        self.reply_markups = []
        self.from_user = DummyUser()
        self.effective_user = self.from_user

    async def reply_text(self, text, **kwargs):
        self.sent_texts.append(text)
        self.reply_markups.append(kwargs.get('reply_markup'))

class DummyDatetime:
    def __init__(self, date_str):
        self.date_str = date_str

    def strftime(self, _):
        return self.date_str

@pytest.mark.asyncio
@patch('app.bots.telegram.commands.history.get_user_history')
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
    await history(dummy_update, dummy_context)

    # Assert that response includes article titles
    assert "Here are your recent topics" in dummy_message.sent_texts[-1]

    buttons = dummy_message.reply_markups[-1].inline_keyboard  # list of lists
    button_texts = [btn.text for row in buttons for btn in row]

    assert "AI Innovations" in button_texts
    assert "Blockchain" in button_texts

@pytest.mark.asyncio
@patch('app.bots.telegram.commands.history.get_user_history')
async def test_history_without_records(mock_get_user_history):
    # Mock empty history for user
    mock_get_user_history.return_value = []

    dummy_message = DummyMessage()
    dummy_update = Update(update_id=5678, message=dummy_message)
    dummy_context = AsyncMock()

    await history(dummy_update, dummy_context)

    # Assert that the bot informs no history is found
    assert "No history found yet" in dummy_message.sent_texts[-1]