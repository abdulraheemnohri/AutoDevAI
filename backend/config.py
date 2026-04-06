import os
from dotenv import load_dotenv

load_dotenv()

# API Settings
API_TIMEOUT = 10
MAX_RETRIES = 3

# Database Settings
DATABASE_PATH = os.getenv("DATABASE_PATH", "database/apis.db")

# GitHub Settings
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPOSITORY = os.getenv("GITHUB_REPOSITORY")

# AI Provider Keys (Optional, system will discover free ones)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
HF_TOKEN = os.getenv("HF_TOKEN")
DEEPINFRA_API_KEY = os.getenv("DEEPINFRA_API_KEY")
