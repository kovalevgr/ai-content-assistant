import pytest
from unittest.mock import patch
from app.agents.topic_aggregator import search_articles_by_topic

@patch('app.agents.topic_aggregator.fetch_rss_articles')
def test_search_articles_by_topic(mock_fetch_articles):
    mock_fetch_articles.return_value = [
        {"title": "AI Innovations in 2024", "summary": "New breakthroughs in AI technology.", "link": "http://example.com/1"},
        {"title": "Space news", "summary": "New mission to Mars", "link": "http://example.com/2"},
        {"title": "AI and healthcare", "summary": "How AI helps doctors", "link": "http://example.com/3"},
    ]

    found_articles = search_articles_by_topic("AI")

    assert len(found_articles) == 2
    assert "AI Innovations" in found_articles[0]["title"]
    assert "AI and healthcare" in found_articles[1]["title"]