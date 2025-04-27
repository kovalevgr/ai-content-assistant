import pytest
from unittest.mock import AsyncMock
from telegram import Update
from app.bots.telegram.commands.start import start

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
async def test_start_command():
    dummy_message = DummyMessage()
    dummy_update = Update(update_id=12345, message=dummy_message)
    dummy_context = AsyncMock()

    # Call /start handler
    await start(dummy_update, dummy_context)

    # Assert that the bot sent any non-empty welcome message
    assert dummy_message.sent_texts, "No message was sent"
    sent_text = dummy_message.sent_texts[-1].lower()

    # Check if the welcome message contains expected keywords
    assert "start" in sent_text or "content" in sent_text or "assistant" in sent_text