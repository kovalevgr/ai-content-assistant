import pytest
from unittest.mock import AsyncMock, patch
from app.agents.image_generator import generate_images

@pytest.mark.asyncio
@patch('openai.resources.Images.acreate', new_callable=AsyncMock)
async def test_generate_images_mock(mock_acreate):
    # Mock DALL-E async response
    mock_acreate.return_value = {
        "data": [{"url": "http://example.com/fake-image1.png"}]
    }

    result = await generate_images(topic="AI Trends", num_images=1)

    assert isinstance(result, list)
    assert len(result) == 1
    assert "fake-image1.png" in result[0]