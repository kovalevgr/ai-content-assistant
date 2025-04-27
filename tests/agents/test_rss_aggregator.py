import pytest
from unittest.mock import patch, MagicMock
from app.agents.rss_aggregator import fetch_rss_articles

@pytest.mark.asyncio
@patch('app.agents.rss_aggregator.feedparser.parse')
async def test_fetch_rss_articles(mock_parse):
    fake_feed = MagicMock()
    fake_feed.entries = [
        MagicMock(title="Test Title 1", summary="Test Summary 1", link="http://example.com/1"),
        MagicMock(title="Test Title 2", summary="Test Summary 2", link="http://example.com/2"),
    ]
    mock_parse.return_value = fake_feed

    articles = fetch_rss_articles(feeds=["http://fake-rss.com"])

    assert len(articles) == 2
    assert articles[0]["title"] == "Test Title 1"
    assert articles[0]["link"] == "http://example.com/1"
    assert "summary" in articles[0]