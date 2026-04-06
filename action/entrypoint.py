import sys
import os

# Add project root to sys.path in a cross-platform manner
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# Use absolute imports for better cross-platform support
from backend.main import run_assistant

if __name__ == "__main__":
    try:
        run_assistant()
    except KeyboardInterrupt:
        print("\n👋 AutoDevAI stopped by user.")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)
