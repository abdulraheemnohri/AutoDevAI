import requests
import json
from backend.config import JULES_API_KEY, API_TIMEOUT

BASE_URL = "https://jules.googleapis.com/v1alpha"

def list_sources():
    """Lists available sources for the Jules API."""
    if not JULES_API_KEY:
        raise ValueError("JULES_API_KEY not found.")

    url = f"{BASE_URL}/sources"
    headers = {"X-Goog-Api-Key": JULES_API_KEY}

    try:
        response = requests.get(url, headers=headers, timeout=API_TIMEOUT)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Jules API list_sources error: {e}")
        raise

def create_session(prompt, source_name, automation_mode="AUTO_CREATE_PR", starting_branch="main", title="New AI Session"):
    """Creates a new session with the Jules API."""
    if not JULES_API_KEY:
        raise ValueError("JULES_API_KEY not found.")

    url = f"{BASE_URL}/sessions"
    headers = {
        "X-Goog-Api-Key": JULES_API_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "prompt": prompt,
        "sourceContext": {
            "source": source_name,
            "githubRepoContext": {
                "startingBranch": starting_branch
            }
        },
        "automationMode": automation_mode,
        "title": title
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=API_TIMEOUT)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Jules API create_session error: {e}")
        raise

def send_message(session_id, prompt):
    """Sends a message to an existing Jules API session."""
    if not JULES_API_KEY:
        raise ValueError("JULES_API_KEY not found.")

    url = f"{BASE_URL}/sessions/{session_id}:sendMessage"
    headers = {
        "X-Goog-Api-Key": JULES_API_KEY,
        "Content-Type": "application/json"
    }
    data = {"prompt": prompt}

    try:
        response = requests.post(url, headers=headers, json=data, timeout=API_TIMEOUT)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Jules API send_message error: {e}")
        raise

def list_activities(session_id, page_size=30):
    """Lists activities in a specific Jules API session."""
    if not JULES_API_KEY:
        raise ValueError("JULES_API_KEY not found.")

    url = f"{BASE_URL}/sessions/{session_id}/activities?pageSize={page_size}"
    headers = {"X-Goog-Api-Key": JULES_API_KEY}

    try:
        response = requests.get(url, headers=headers, timeout=API_TIMEOUT)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Jules API list_activities error: {e}")
        raise

def generate_jules(prompt):
    """Simplified generate function to fit the existing router pattern."""
    # This is a bit complex as Jules is session-based, but we'll attempt
    # to find a default source and create a one-off session.
    # For now, it will act as a wrapper to list sources and create a session.
    try:
        sources = list_sources()
        if not sources or "sources" not in sources or not sources["sources"]:
            raise ValueError("No Jules sources available.")

        source_name = sources["sources"][0]["name"]
        session = create_session(prompt, source_name)
        return f"Jules Session created: {session.get('id', 'Unknown')}. You can track activities separately."
    except Exception as e:
        print(f"Jules generate error: {e}")
        raise
