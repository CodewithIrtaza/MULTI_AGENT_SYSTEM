import os
import requests

from langchain_core.tools import tool
from langchain_groq import ChatGroq
from bs4 import BeautifulSoup
from tavily import TavilyClient


from rich import print
from dotenv import load_dotenv
load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def search_web(query: str) -> str:
    """
    Search the web for recent and reliable information on a topic . Returns Titles , URLs and snippets.
    """

    response = tavily.search(
        query = query, 
        max_results = 5
    )

    out = []
    for result in response["results"]:
        out.append( 
        f"Title: {result['title']}\nURL: {result['url']}\nSnippet: {result['content'][:300]}\n"
        )
    return "\n----\n".join(out)


@tool
def scrape_url(url: str) -> str:
    """                                                                                             
        Scrape a webpage and return its text content.                                                   
        Use this tool to read/fetch content from any URL.                                               
        This is the ONLY tool available for web access.                                                 
        """  
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"}
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()
        return soup.get_text(separator="\n", strip=True)[:5000]
    except Exception as e:
        return f"Error scraping {url}: {e}"


