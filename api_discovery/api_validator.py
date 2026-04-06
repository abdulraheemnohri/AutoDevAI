import requests
import time
import sqlite3
from backend.config import DATABASE_PATH, API_TIMEOUT

def validate_endpoint(endpoint):
    """Validate an API endpoint by sending a small, structured request."""
    print(f"🧪 Validating endpoint: {endpoint}")
    
    # Simple test payload (OpenAI-compatible)
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": "hi"}],
        "max_tokens": 5
    }
    
    start_time = time.time()
    try:
        response = requests.post(endpoint, json=payload, timeout=API_TIMEOUT)
        latency = time.time() - start_time
        
        if response.status_code == 200:
            result = response.json()
            # Verify basic OpenAI-like structure
            if 'choices' in result and len(result['choices']) > 0:
                print(f"✅ Endpoint {endpoint} is working! Latency: {latency:.2f}s")
                return True, latency
            else:
                print(f"⚠️ Endpoint {endpoint} returned successful code but unexpected JSON structure: {result}")
                return False, latency
        else:
            print(f"❌ Endpoint {endpoint} returned status code: {response.status_code}")
            return False, latency
    except Exception as e:
        print(f"❌ Endpoint {endpoint} validation failed: {e}")
        return False, 0.0

def validate_all_apis():
    """Validate all APIs in the database and update their status."""
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    c.execute("SELECT id, endpoint FROM apis")
    apis = c.fetchall()
    
    for api_id, endpoint in apis:
        is_valid, latency = validate_endpoint(endpoint)
        status = 'active' if is_valid else 'inactive'
        
        c.execute("""
            UPDATE apis 
            SET status = ?, latency = ?, last_checked = CURRENT_TIMESTAMP 
            WHERE id = ?
        """, (status, latency, api_id))
        
    conn.commit()
    conn.close()
    print("✅ All APIs in database validated.")
