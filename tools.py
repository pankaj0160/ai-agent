import json
import requests
import streamlit as st
from urllib.parse import urlparse
from tavily import TavilyClient
from langchain.tools import tool

OPENWEATHER_API_KEY = st.secrets["OPENWEATHER_API_KEY"]
TAVILY_API_KEY = st.secrets["TAVILY_API_KEY"]

tavily_client = TavilyClient(api_key=TAVILY_API_KEY)


@tool
def get_weather(city: str) -> str:
    """
    Get current weather information for a city.
    Returns structured JSON for rich dashboard rendering.
    """
    try:
        url = (
            "https://api.openweathermap.org/data/2.5/weather"
            f"?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
        )

        response = requests.get(url, timeout=12)
        response.raise_for_status()

        data = response.json()

        weather = {
            "city": data.get("name", city.title()),
            "country": data.get("sys", {}).get("country", ""),
            "temp": round(data.get("main", {}).get("temp", 0), 1),
            "feels_like": round(data.get("main", {}).get("feels_like", 0), 1),
            "humidity": data.get("main", {}).get("humidity", 0),
            "pressure": data.get("main", {}).get("pressure", 0),
            "wind_speed": round(data.get("wind", {}).get("speed", 0), 1),
            "visibility": data.get("visibility", 0),
            "condition": data.get("weather", [{}])[0].get("description", "Unknown").title(),
        }

        return json.dumps(weather)

    except Exception as e:
        return f"Weather tool error: {str(e)}"


@tool
def get_news(topic: str) -> str:
    """
    Get latest breaking news for a city or topic.
    Returns structured JSON list for beautiful card rendering.
    """
    try:
        query = f"breaking latest news in {topic}"

        response = tavily_client.search(
            query=query,
            search_depth="advanced",
            max_results=6,
        )

        results = response.get("results", [])

        if not results:
            return json.dumps({"topic": topic, "news": []})

        news_items = []

        for item in results:
            url = item.get("url", "")
            domain = "Source"

            try:
                if url:
                    domain = urlparse(url).netloc.replace("www.", "")
            except:
                pass

            content = item.get("content", "")

            news_items.append({
                "title": item.get("title", "No title"),
                "summary": content[:280] + ("..." if len(content) > 280 else ""),
                "url": url,
                "source": domain,
            })

        return json.dumps({
            "topic": topic,
            "news": news_items
        })

    except Exception as e:
        return f"News tool error: {str(e)}"