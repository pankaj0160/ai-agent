def format_news(news_articles):
    formatted = []

    for article in news_articles:
        formatted.append({
            "title": article["title"],
            "summary": article["content"],
            "url": article["url"]
        })

    return formatted