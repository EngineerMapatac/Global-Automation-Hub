import requests
import os

# This script checks if your token can see your full list of repos
TOKEN = os.getenv("GH_PAT")
headers = {"Authorization": f"token {TOKEN}"}

# We use /user/repos to get all repos the token has access to
response = requests.get("https://api.github.com/user/repos", headers=headers)

if response.status_code == 200:
    repos = response.json()
    print(f"✅ Success! Your token can see {len(repos)} repositories.")
    for repo in repos:
        print(f" - {repo['name']}")
else:
    print(f"❌ Connection failed. Status code: {response.status_code}")