from app.agents.rss_aggregator import fetch_rss_articles

def search_articles_by_topic(topic: str, feeds=None, max_articles_per_feed=5) -> list:
    """Search for articles that match the given topic in title or summary."""
    topic = topic.lower()
    found_articles = []

    articles = fetch_rss_articles(feeds=feeds, max_articles=max_articles_per_feed)

    for article in articles:
        title = article.get("title", "").lower()
        summary = article.get("summary", "").lower()

        if topic in title or topic in summary:
            found_articles.append(article)

    return found_articles