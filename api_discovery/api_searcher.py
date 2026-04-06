import sqlite3
from search_engines.duckduckgo import search as ddg_search
from search_engines.brave import search as brave_search
from search_engines.searx import search as searx_search
from search_engines.bing import search as bing_search
from browser_agent.crawler import crawl
from api_discovery.endpoint_extractor import extract
from api_discovery.api_validator import validate_endpoint
from backend.config import DATABASE_PATH

def discover_apis():
    """Search for new AI APIs across multiple search engines, validate them, and store them."""
    print("🔍 Starting multi-engine API discovery process...")
    
    queries = [
        "free llm api endpoint",
        "openai compatible api endpoint",
        "free ai inference api",
        "public chat completions api"
    ]
    
    search_engines = [
        ("DuckDuckGo", ddg_search),
        ("Brave Search", brave_search),
        ("SearX", searx_search),
        ("Bing", bing_search)
    ]

    all_discovered_links = []
    
    for query in queries:
        for engine_name, search_func in search_engines:
            print(f"🌍 Querying {engine_name} for: {query}")
            links = search_func(query)
            all_discovered_links.extend(links)

    # Deduplicate and crawl
    unique_links = list(set(all_discovered_links))
    print(f"🔎 Found {len(unique_links)} unique search results. Scraping...")

    all_potential_endpoints = []
    for link in unique_links[:20]: # Limit crawling to top results
        print(f"📄 Scraping link: {link}")
        page_text = crawl(link)
        endpoints = extract(page_text)
        all_potential_endpoints.extend(endpoints)
            
    # Deduplicate and validate
    unique_endpoints = list(set(all_potential_endpoints))
    print(f"🔎 Found {len(unique_endpoints)} potential endpoints. Validating...")
    
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    
    for endpoint in unique_endpoints:
        # Check if already in database
        c.execute("SELECT id FROM apis WHERE endpoint = ?", (endpoint,))
        if c.fetchone():
            print(f"⏭️ Endpoint {endpoint} already in database. Skipping.")
            continue
            
        is_valid, latency = validate_endpoint(endpoint)
        if is_valid:
            print(f"✨ Storing new working API: {endpoint}")
            c.execute("""
                INSERT INTO apis (endpoint, provider, success_rate, latency, status)
                VALUES (?, ?, ?, ?, ?)
            """, (endpoint, "Discovered", 1.0, latency, "active"))
            
    conn.commit()
    conn.close()
    print("✅ Multi-engine API discovery process complete.")
