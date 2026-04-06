import os
import json
import requests
from github_bot.command_parser import parse_command
from ai_engine.router import generate
from ai_engine.prompt_builder import build_prompt
from backend.config import GITHUB_TOKEN

def process_events():
    """Process GitHub events from environment variables (GitHub Actions)."""
    event_path = os.getenv("GITHUB_EVENT_PATH")
    if not event_path:
        print("⚠️ GITHUB_EVENT_PATH not found. Skipping event processing.")
        return

    with open(event_path, "r") as f:
        event_data = json.load(f)

    # Check for issue_comment event
    if "comment" in event_data:
        comment_body = event_data["comment"]["body"]
        comment_id = event_data["comment"]["id"]
        issue_url = event_data["issue"]["url"]

        command, args = parse_command(comment_body)
        
        if command:
            print(f"🤖 AI Command detected: {command} with args: {args}")

            # Use build_prompt to create a structured prompt
            prompt = build_prompt(command, args)
            response_text = generate(prompt)

            print(f"🤖 AI Response: {response_text}")

            # Post the response back to GitHub
            post_comment(issue_url, response_text)
    else:
        print("ℹ️ No AI command detected in GitHub event.")

def post_comment(issue_url, message):
    """Post a comment back to a GitHub issue or PR."""
    if not GITHUB_TOKEN:
        print("⚠️ GITHUB_TOKEN not found. Cannot post comment.")
        return

    url = f"{issue_url}/comments"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {"body": message}

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        print(f"✅ Comment posted successfully.")
    except Exception as e:
        print(f"❌ Error posting comment: {e}")

def handle_command(command, args, event_data):
    """Handle specific AI commands (Deprecated in favor of build_prompt and generate directly)."""
    # This function is kept for backward compatibility if needed,
    # but the logic is now in process_events using build_prompt and generate.
    prompt = build_prompt(command, args)
    return generate(prompt)
