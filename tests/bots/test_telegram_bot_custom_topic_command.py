from unittest.mock import AsyncMock, patch

import pytest
from telegram import Update

from app.bots.telegram.commands.custom_topic import custom_topic
from app.bots.telegram.handlers.handle_article_decision import handle_article_decision
from app.bots.telegram.handlers.handle_message import handle_message
from app.bots.telegram.state import user_states, user_temp_data


class DummyUser:
    def __init__(self, user_id=123456):
        self.id = user_id

class DummyMessage:
    def __init__(self):
        self.sent_texts = []
        self.from_user = DummyUser()
        self.effective_user = DummyUser()

    async def reply_text(self, text, **kwargs):
        self.sent_texts.append(text)

class DummyCallbackQuery:
    def __init__(self, data, message):
        self.data = data
        self.message = message
        self.from_user = message.effective_user

    async def answer(self):
        pass

    async def edit_message_text(self, text, **kwargs):
        self.message.sent_texts.append(text)

@pytest.mark.asyncio
@patch('app.db.crud.save_article_history')
@patch('app.bots.telegram.handlers.handle_message.search_articles_by_topic')
@patch('app.bots.telegram.handlers.handle_message.summarize_articles')
@patch('app.bots.telegram.handlers.handle_message.rewrite_text')
@patch('app.bots.telegram.handlers.handle_message.generate_images')
async def test_custom_topic_flow(
    mock_generate_images,
    mock_rewrite_text,
    mock_summarize_articles,
    mock_search_articles,
    mock_save_history
):
    # Mock search_articles
    mock_search_articles.return_value = [
        {"title": "AI Innovations", "summary": "Changing the world.", "link": "http://example.com/ai-news"}
    ]

    # Mock summarize_articles
    mock_summarize_articles.return_value = "Summarized text about AI."

    # Mock generate_images
    mock_generate_images.return_value = ["http://example.com/image1.png"]

    # Mock rewrite_text
    mock_rewrite_text.return_value = "Rewritten casual text about AI with an image."

    # Dummy Telegram objects
    dummy_message = DummyMessage()
    dummy_update = Update(update_id=1234, message=dummy_message)
    dummy_context = AsyncMock()

    # Step 1: User sends /custom_topic
    await custom_topic(dummy_update, dummy_context)
    assert "Please type the topic" in dummy_message.sent_texts[-1]

    # Step 2: User enters topic
    dummy_message.sent_texts = []
    dummy_update.message.text = "AI innovations"

    user_states[dummy_update.effective_user.id] = "awaiting_topic"

    await handle_message(dummy_update, dummy_context)
    assert "choose a writing style" in dummy_message.sent_texts[-1].lower()

    # Step 3: User selects style
    dummy_message.sent_texts = []
    dummy_update.message.text = "casual"
    user_states[dummy_update.effective_user.id] = "awaiting_style"

    await handle_message(dummy_update, dummy_context)

    # Check rewritten text with embedded image link
    combined_text = " ".join(dummy_message.sent_texts).lower()
    assert "rewritten casual text" in combined_text

    # Check that article approval question appeared
    assert any("what would you like to do" in text.lower() for text in dummy_message.sent_texts)

@pytest.mark.asyncio
async def test_start_custom_topic_flow():
    dummy_message = DummyMessage()
    dummy_update = Update(update_id=1, message=dummy_message)
    dummy_context = AsyncMock()

    await custom_topic(dummy_update, dummy_context)

    assert "please type the topic" in dummy_message.sent_texts[-1].lower()
    assert user_states[dummy_message.effective_user.id] == "awaiting_topic"

@pytest.mark.asyncio
@patch('app.bots.telegram.handlers.handle_message.search_articles_by_topic')
async def test_handle_topic_input(mock_search_articles):
    mock_search_articles.return_value = [{"title": "test", "link": "http://example.com"}]

    dummy_message = DummyMessage()
    dummy_update = Update(update_id=2, message=dummy_message)
    dummy_context = AsyncMock()

    user_states[dummy_message.effective_user.id] = "awaiting_topic"

    dummy_update.message.text = "AI trends"
    await handle_message(dummy_update, dummy_context)

    assert "choose a writing style" in dummy_message.sent_texts[-1].lower()
    assert user_states[dummy_message.effective_user.id] == "awaiting_style"

@pytest.mark.asyncio
@patch('app.bots.telegram.handlers.handle_message.summarize_articles')
@patch('app.bots.telegram.handlers.handle_message.generate_images')
@patch('app.bots.telegram.handlers.handle_message.rewrite_text')
@patch('app.db.crud.save_article_history')
async def test_handle_style_input_and_article_generation(
    mock_save_history, mock_rewrite_text, mock_generate_images, mock_summarize_articles
):
    mock_summarize_articles.return_value = "Summarized content"
    mock_generate_images.return_value = ["http://example.com/image1.png"]
    mock_rewrite_text.return_value = "Rewritten article with images"

    dummy_message = DummyMessage()
    dummy_update = Update(update_id=3, message=dummy_message)
    dummy_context = AsyncMock()

    user_states[dummy_message.effective_user.id] = "awaiting_style"
    user_temp_data[dummy_message.effective_user.id] = {
        "topic": "AI innovations",
        "articles": [{"title": "Example", "link": "http://example.com"}]
    }

    dummy_update.message.text = "professional"

    await handle_message(dummy_update, dummy_context)

    combined_text = " ".join(dummy_message.sent_texts).lower()

    assert "here’s a" in combined_text
    assert "what would you like to do" in combined_text

@pytest.mark.asyncio
async def test_handle_edit_article():
    dummy_message = DummyMessage()
    dummy_callback_query = DummyCallbackQuery(data="edit_article", message=dummy_message)
    dummy_update = Update(update_id=5, callback_query=dummy_callback_query)
    dummy_context = AsyncMock()

    await handle_article_decision(dummy_update, dummy_context)

    sent_texts = " ".join(dummy_message.sent_texts).lower()
    assert "please send the corrected text" in sent_texts
    assert user_states[dummy_message.effective_user.id] == "awaiting_correction"
