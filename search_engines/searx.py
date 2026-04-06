import requests
from bs4 import BeautifulSoup

def search(query):
    """Search a SearX instance and return results."""
    print(f"🔎 Searching SearX for: {query}")

    # Public SearX instance for demonstration
    url = f"https://searx.be/search?q={query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract links from search results (this is speculative as instance UI varies)
        links = []
        for a in soup.find_all('a'):
            href = a.get('href')
            if href and href.startswith('http') and 'searx' not in href:
                links.append(href)

        # Deduplicate and limit
        return list(set(links))[:10]
    except Exception as e:
        print(f"⚠️ SearX search failed: {e}")
        return []
