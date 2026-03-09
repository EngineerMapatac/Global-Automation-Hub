import requests
import os

HUB_REPO_NAME = "Global-Automation-Hub" # We skip this so it doesn't trigger itself

def get_all_repos(headers):
    """Fetches all repositories owned by the authenticated user."""
    repos = []
    # Using per_page=100 handles up to 100 repos. 
    url = "https://api.github.com/user/repos?type=owner&per_page=100"
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        for repo in response.json():
            # Skip the hub repository itself
            if repo['name'] != HUB_REPO_NAME:
                repos.append(repo['full_name'])
        return repos
    else:
        print(f"❌ Failed to fetch repositories: {response.status_code} - {response.text}")
        return []

def main():
    token = os.getenv("GH_PAT")
    if not token:
        print("❌ Error: GH_PAT environment variable is missing.")
        return

    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {token}"
    }
    
    print("🔍 Fetching all repositories...")
    target_repos = get_all_repos(headers)
    
    if not target_repos:
        print("⚠️ No repositories found or failed to fetch.")
        return
        
    print(f"🎯 Found {len(target_repos)} repositories. Sending signals...")
    
    # This is the signal each repo is listening for
    payload = {"event_type": "global_sync_trigger"}

    for repo in target_repos:
        url = f"https://api.github.com/repos/{repo}/dispatches"
        r = requests.post(url, headers=headers, json=payload)
        
        if r.status_code == 204:
            print(f"✅ Signal sent to {repo}")
        else:
            print(f"❌ Failed {repo}: {r.status_code} - {r.text}")

if __name__ == "__main__":
    main()