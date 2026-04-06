import requests
from bs4 import BeautifulSoup

def search(query):
    """Search Bing (HTML version) and return results."""
    print(f"🔎 Searching Bing for: {query}")

    url = f"https://www.bing.com/search?q={query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract links from search results
        links = []
        for a in soup.find_all('a'):
            href = a.get('href')
            if href and href.startswith('http') and 'bing.com' not in href and 'microsoft.com' not in href:
                links.append(href)

        # Deduplicate and limit
        return list(set(links))[:10]
    except Exception as e:
        print(f"⚠️ Bing search failed: {e}")
        return []
