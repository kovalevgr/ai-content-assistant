import feedparser

from app.agents.rss_sources import DEFAULT_RSS_FEEDS

def fetch_rss_articles(feeds=None, max_articles=5):
    if feeds is None:
        feeds = DEFAULT_RSS_FEEDS

    articles = []

    for feed_url in feeds:
        parsed_feed = feedparser.parse(feed_url)
        for entry in parsed_feed.entries[:max_articles]:
            articles.append({
                "title": entry.title,
                "summary": entry.summary if hasattr(entry, 'summary') else '',
                "link": entry.link
            })

    return articles