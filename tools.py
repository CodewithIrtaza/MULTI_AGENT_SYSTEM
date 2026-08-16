import os
import requests
import json

from langchain_core.tools import tool
from langchain_groq import ChatGroq
from bs4 import BeautifulSoup
from apify_client import ApifyClient

from rich import print
from dotenv import load_dotenv
load_dotenv()


@tool
def search_web(query: str) -> str:
    """
    Search the web for recent and reliable information on a topic . Returns Titles , URLs and snippets.
    """

    url = "https://google.serper.dev/search"
    payload = json.dumps({
      "q": query,
      "num": 3
    })
    headers = {
      'X-API-KEY': os.getenv("SERPER_API_KEY"),
      'Content-Type': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    
    if response.status_code != 200:
        return f"Error: Failed to fetch search results. Status code {response.status_code}"
    
    data = response.json()

    out = []
    for result in data.get("organic", [])[:5]:
        out.append( 
        f"Title: {result.get('title', '')}\nURL: {result.get('link', '')}\nSnippet: {result.get('snippet', '')[:300]}\n"
        )
    return "\n----\n".join(out)


@tool
def scrape_url(url: str) -> str:
    """
    Scrape a webpage and return its text content.
    Use this tool to read/fetch content from any URL.
    This is the ONLY tool available for web access.
    """
    try:
        client = ApifyClient(os.getenv("APIFY_API_TOKEN"))
        
        run_input = {
            "startUrls": [{"url": url.strip()}],
            "maxCrawlPages": 1,
            "crawlerType": "cheerio"
        }
        
        # Run the actor and wait for it to finish
        run = client.actor("apify/website-content-crawler").call(run_input=run_input)
        
        # Fetch results from the actor's default dataset
        text_content = ""
        for item in client.dataset(run.default_dataset_id).iterate_items():
            text_content += item.get("text", "") + "\n"
            
        return text_content[:5000] if text_content else "No content found."
    except Exception as e:
        return f"Error scraping {url}: {e}"

