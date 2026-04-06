import sqlite3
from search_engines.duckduckgo import search
from browser_agent.crawler import crawl
from api_discovery.endpoint_extractor import extract
from api_discovery.api_validator import validate_endpoint
from backend.config import DATABASE_PATH

def discover_apis():
    """Search for new AI APIs, validate them, and store them in the database."""
    print("🔍 Starting API discovery process...")
    
    queries = [
        "free llm api endpoint",
        "openai compatible api endpoint",
        "free ai inference api",
        "public chat completions api"
    ]
    
    all_discovered_endpoints = []
    
    for query in queries:
        links = search(query)
        for link in links:
            print(f"📄 Scraping link: {link}")
            page_text = crawl(link)
            endpoints = extract(page_text)
            all_discovered_endpoints.extend(endpoints)
            
    # Deduplicate and validate
    unique_endpoints = list(set(all_discovered_endpoints))
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
    print("✅ API discovery process complete.")
