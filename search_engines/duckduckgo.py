import requests
from bs4 import BeautifulSoup

def search(query):
    """Search DuckDuckGo and return a list of page contents/URLs."""
    print(f"🔎 Searching DuckDuckGo for: {query}")
    url = f"https://html.duckduckgo.com/html/?q={query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract links from search results
        links = []
        for a in soup.find_all('a', class_='result__a'):
            href = a.get('href')
            if href:
                links.append(href)
        
        return links
    except Exception as e:
        print(f"⚠️ DuckDuckGo search failed: {e}")
        return []
