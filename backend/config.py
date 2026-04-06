import os
from dotenv import load_dotenv

load_dotenv()

# Base directory for the project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# API Settings
API_TIMEOUT = 10
MAX_RETRIES = 3

# Database Settings
# Use cross-platform path joining
DEFAULT_DB_PATH = os.path.join(BASE_DIR, "database", "apis.db")
DATABASE_PATH = os.getenv("DATABASE_PATH", DEFAULT_DB_PATH)

# GitHub Settings
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPOSITORY = os.getenv("GITHUB_REPOSITORY")

# AI Provider Keys (Optional, system will discover free ones)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
HF_TOKEN = os.getenv("HF_TOKEN")
DEEPINFRA_API_KEY = os.getenv("DEEPINFRA_API_KEY")
