from browser_agent.crawler import crawl
from browser_agent.page_parser import parse_page_for_docs, extract_code_snippets
from api_discovery.endpoint_extractor import extract
import sqlite3
from backend.config import DATABASE_PATH

def scan_documentation_site(url):
    """Specifically targets and scans documentation for AI-related patterns and endpoints."""
    print(f"📄 Scanning documentation site: {url}")

    # 1. Crawl the page
    # In a real scenario, this would use Playwright directly or a more robust wrapper
    text = crawl(url)

    if not text:
        return []

    # 2. Extract potential endpoints
    endpoints = extract(text)

    # 3. Store in knowledge engine (optional, for later context)
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        c = conn.cursor()
        c.execute("""
            INSERT OR REPLACE INTO knowledge (source, content, tags)
            VALUES (?, ?, ?)
        """, (url, text, "documentation,ai_provider"))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"❌ Error storing scanned doc in knowledge base: {e}")

    return endpoints
