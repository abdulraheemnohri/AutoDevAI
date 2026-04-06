import subprocess
import os

def run_git_command(args, repo_path=None):
    """Run a git command and return the output."""
    try:
        result = subprocess.run(
            ["git"] + args,
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"❌ Git command failed: {e.stderr}")
        return None

def create_branch(branch_name, repo_path=None):
    """Create and checkout a new git branch."""
    print(f"🌿 Creating branch: {branch_name}")
    return run_git_command(["checkout", "-b", branch_name], repo_path) is not None

def commit_changes(message, repo_path=None):
    """Stage all changes and commit them."""
    print(f"💾 Committing changes: {message}")
    run_git_command(["add", "."], repo_path)
    return run_git_command(["commit", "-m", message], repo_path) is not None

def push_to_github(branch_name, repo_path=None):
    """Push the specified branch to GitHub."""
    print(f"🚀 Pushing branch to origin: {branch_name}")
    # Note: Requires proper GITHUB_TOKEN setup for authentication
    return run_git_command(["push", "origin", branch_name], repo_path) is not None

def clone_repository(repo_url, target_path):
    """Clone a GitHub repository to a specific path."""
    print(f"📥 Cloning repository: {repo_url}")
    return run_git_command(["clone", repo_url, target_path]) is not None
