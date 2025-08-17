import webbrowser
from typing import Optional
from langchain.tools import BaseTool
import urllib.parse

def search_google(query: str, open_browser: bool = False) -> str:
    encoded_query = urllib.parse.quote(query)
    if open_browser:
        webbrowser.open(f"https://www.google.com/search?q={encoded_query}")
        return f"Opening browser with search for: {query}"
    else:
        return f"Here's the search link for {query}: https://www.google.com/search?q={encoded_query}"

class GoogleSearchTool(BaseTool):
    name: str = "google_search"
    description: str = "Searches Google for a query. Set open_browser to true to open the default web browser."
    
    def _run(self, query: str, open_browser: bool = False) -> str:
        return search_google(query, open_browser)
    
    def _arun(self, query: str, open_browser: bool = False) -> str:
        raise NotImplementedError("Async not implemented")

google_search = GoogleSearchTool()
