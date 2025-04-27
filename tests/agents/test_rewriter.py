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
                    "content": "This is a rewritten version of the text."
                }
            }
        ]
    }

    original_text = "AI is transforming industries."
    rewritten = await rewrite_text(original_text, style="casual")

    assert "rewritten version" in rewritten
    mock_acreate.assert_called_once()