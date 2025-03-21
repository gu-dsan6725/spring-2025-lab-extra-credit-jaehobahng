"""
Google Search MCP Server
This server provides MCP tools to search google using the Google Custom Search API.
"""

import requests
from dotenv import load_dotenv

import os
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Union

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field
from tabulate import tabulate
import requests
from readability import Document
from bs4 import BeautifulSoup


load_dotenv()  # Loads variables from .env into the environment

# Initialize FastMCP server
mcp = FastMCP("google_search")

google_api = os.getenv("google_api")
search_engine = os.getenv("search_engine")
# query = "Python Google Search API"

@mcp.tool()
async def search_google(query):
    """
    Search Google using the Google Custom Search API.

    Args:
        query: the query to search for with the google search api

    Returns:
        A list with the main content of the retrieved links
    """
    url = f"https://www.googleapis.com/customsearch/v1"
    params = {
        "q": query,
        "key": google_api,
        "cx": search_engine,
        "num": 2  # Number of results
    }

    response = requests.get(url, params=params)
    data = response.json()

    content = []

    # Print search results
    for i, item in enumerate(data.get("items", []), start=1):
        # print(f"{i}. {item['title']}")
        # print(f"   {item['link']}\n")

        # url = "https://stackoverflow.com/questions/37083058/programmatically-searching-google-in-python-using-custom-search"
        url = item['link']
        headers = {"User-Agent": "Mozilla/5.0"}

        response = requests.get(url, headers=headers)
        doc = Document(response.text)

        # Extract main readable content
        main_html = doc.summary()

        # Optional: Clean with BeautifulSoup
        soup = BeautifulSoup(main_html, "html.parser")
        clean_text = soup.get_text(separator="\n", strip=True)

        content.append(clean_text)
    
    return content


def main():
    # Run the server with SSE transport
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()