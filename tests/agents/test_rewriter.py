import pytest
from unittest.mock import AsyncMock, patch
from app.agents.rewriter import rewrite_text

@pytest.mark.asyncio
@patch('app.agents.rewriter.openai.ChatCompletion.acreate', new_callable=AsyncMock)
async def test_rewrite_text(mock_acreate):
    mock_acreate.return_value = {
        "choices": [
            {
                "message": {
                    "content": "This is a rewritten version of the text with images."
                }
            }
        ]
    }

    original_text = "AI is transforming industries."
    images = ["http://example.com/image1.png"]

    rewritten = await rewrite_text(original_text, style="casual", images=images)

    # Assertions
    assert "rewritten version" in rewritten
    mock_acreate.assert_called_once()

    called_args = mock_acreate.call_args[1]["messages"][1]["content"]

    assert "Insert [Image1]" in called_args
    assert "http://example.com/image1.png" in called_args

@pytest.mark.asyncio
@patch('app.agents.rewriter.openai.ChatCompletion.acreate', new_callable=AsyncMock)
async def test_rewrite_text_without_images(mock_acreate):
    mock_acreate.return_value = {
        "choices": [{"message": {"content": "Rewritten text."}}]
    }

    rewritten = await rewrite_text("Some text", style="casual")

    assert "Rewritten" in rewritten
    mock_acreate.assert_called_once()

@pytest.mark.asyncio
async def test_rewrite_text_empty_input():
    rewritten = await rewrite_text("", style="professional")

    assert rewritten == "No text provided for rewriting."

@pytest.mark.asyncio
@patch('app.agents.rewriter.openai.ChatCompletion.acreate', new_callable=AsyncMock)
async def test_rewrite_text_openai_error(mock_acreate):
    mock_acreate.side_effect = Exception("OpenAI API failure")

    original_text = "AI will change the world."
    rewritten = await rewrite_text(original_text, style="casual")

    assert rewritten == original_text  # Falls back to original