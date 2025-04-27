import pytest
from telegram import Update
from app.bots.telegram_bot import start

class DummyMessage:
    def __init__(self):
        self.text = None

    async def reply_text(self, text):
        self.text = text
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