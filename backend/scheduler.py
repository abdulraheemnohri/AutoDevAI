import time
import threading
import sys
import os

# Add project root to sys.path for cross-platform imports
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from api_discovery.api_searcher import discover_apis
from api_discovery.api_validator import validate_all_apis

def start_scheduler():
    """Start background tasks for periodic API discovery and validation."""
    print("📅 Background scheduler starting...")
    
    def discovery_job():
        while True:
            try:
                print("⏰ Running scheduled API discovery...")
                discover_apis()
            except Exception as e:
                print(f"❌ Scheduled API discovery failed: {e}")
            time.sleep(6 * 3600)  # Every 6 hours

    def validation_job():
        while True:
            try:
                print("⏰ Running scheduled API validation...")
                validate_all_apis()
            except Exception as e:
                print(f"❌ Scheduled API validation failed: {e}")
            time.sleep(24 * 3600)  # Every 24 hours

    # Start threads for periodic tasks
    discovery_thread = threading.Thread(target=discovery_job, name="APIDiscoveryThread", daemon=True)
    validation_thread = threading.Thread(target=validation_job, name="APIValidationThread", daemon=True)

    discovery_thread.start()
    validation_thread.start()
    print("✅ Background scheduler active (Discovery every 6h, Validation every 24h).")
