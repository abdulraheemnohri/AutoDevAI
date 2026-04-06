import time
import threading
from api_discovery.api_searcher import discover_apis
from api_discovery.api_validator import validate_all_apis

def start_scheduler():
    """Start background tasks for periodic API discovery and validation."""
    
    def discovery_job():
        while True:
            print("⏰ Running scheduled API discovery...")
            discover_apis()
            time.sleep(6 * 3600)  # Every 6 hours

    def validation_job():
        while True:
            print("⏰ Running scheduled API validation...")
            validate_all_apis()
            time.sleep(24 * 3600)  # Every 24 hours

    # Start threads for periodic tasks
    discovery_thread = threading.Thread(target=discovery_job, daemon=True)
    validation_thread = threading.Thread(target=validation_job, daemon=True)

    discovery_thread.start()
    validation_thread.start()
    print("📅 Background scheduler started.")
