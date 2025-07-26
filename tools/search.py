# tools/search.py

from langchain.tools import tool
import requests
from urllib.parse import quote
import json

@tool
def search_web(query: str) -> str:
    """Search the web using DuckDuckGo Instant Answer API."""
    try:
        # Use DuckDuckGo Instant Answer API (no API key required)
        encoded_query = quote(query)
        url = f"https://api.duckduckgo.com/?q={encoded_query}&format=json&no_html=1&skip_disambig=1"
        
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            # Try to get instant answer
            if data.get('Abstract'):
                return f"Search result for '{query}':\n{data['Abstract']}"
            elif data.get('Definition'):
                return f"Definition of '{query}':\n{data['Definition']}"
            elif data.get('Answer'):
                return f"Answer for '{query}': {data['Answer']}"
            elif data.get('RelatedTopics') and len(data['RelatedTopics']) > 0:
                topics = []
                for topic in data['RelatedTopics'][:3]:  # First 3 topics
                    if isinstance(topic, dict) and 'Text' in topic:
                        topics.append(topic['Text'])
                if topics:
                    return f"Search results for '{query}':\n" + "\n\n".join(topics)
            
            return f"No detailed results found for '{query}'. Try a more specific search term."
        else:
            return f"Search service unavailable (status {response.status_code})"
            
    except requests.exceptions.Timeout:
        return "Search timeout. Please try again."
    except requests.exceptions.ConnectionError:
        return "Unable to connect to search service. Check your internet connection."
    except Exception as e:
        return f"Search error: {e}"

@tool
def get_news_headlines() -> str:
    """Get current news headlines."""
    try:
        # Using a free news API (you might want to get an API key for better results)
        url = "https://newsapi.org/v2/top-headlines?country=us&apiKey=demo"
        
        # Note: This is a demo key with limited functionality
        # For production, get a free API key from newsapi.org
        
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('articles'):
                headlines = []
                for article in data['articles'][:5]:  # Top 5 headlines
                    title = article.get('title', 'No title')
                    source = article.get('source', {}).get('name', 'Unknown source')
                    headlines.append(f"• {title} ({source})")
                
                if headlines:
                    return "Top News Headlines:\n" + "\n".join(headlines)
            
            return "No news headlines available at the moment."
        else:
            return "News service unavailable. For full news access, configure a NewsAPI key."
            
    except Exception as e:
        return f"Error getting news: {e}"
