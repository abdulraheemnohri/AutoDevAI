import sys
import os

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from github_bot.webhook_handler import process_events
from api_discovery.api_searcher import discover_apis
from database.db_init import init_db
from backend.scheduler import start_scheduler

def run_assistant():
    """Main entry point for the AI Dev Assistant."""
    print("🚀 Starting Self-Expanding AI Dev Assistant...")

    # 1. Initialize Database
    init_db()

    # 2. Discover APIs (Initial run)
    print("🔍 Running initial API discovery...")
    discover_apis()

    # 3. Start Background Scheduler (Optional for long-running processes)
    # start_scheduler()

    # 4. Process GitHub Events
    print("🤖 Processing GitHub events...")
    process_events()

    print("✅ AI Dev Assistant run complete.")

if __name__ == "__main__":
    run_assistant()
