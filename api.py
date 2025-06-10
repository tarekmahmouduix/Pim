import requests, os
import base64 as base
import subprocess

from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise RuntimeError("GitHub token not found. Please set the TOKEN environment variable.")

HEADERS = {"Authorization": f"token {TOKEN}"} # User's token
username = requests.get("https://api.github.com/user", headers=HEADERS).json()["login"]

def get_repos():
    res = requests.get("https://api.github.com/user/repos", headers=HEADERS)
    return res.json() if res.status_code == 200 else []

def delete_repo(repo_name):
    url = f"https://api.github.com/repos/{username}/{repo_name}"
    response = requests.delete(url, headers=HEADERS)
    return response.json() if response.status_code == 204 else None

def star_repo(repo_name):
    url = f"https://api.github.com/user/starred/{username}/{repo_name}"
    response = requests.put(url, headers=HEADERS)
    return response.json() if response.status_code == 201 else None

def create_repo(repo_name):
    url = "https://api.github.com/user/repos"
    data = {"name": repo_name}
    response = requests.post(url, json=data, headers=HEADERS)
    if response.status_code == 201:
        return response.json()
    else:
        print("Failed to create repo:", response.status_code, response.text)
        return None
    
def init_repo(repo_name):
    url = f"https://api.github.com/repos/{username}/{repo_name}/contents/README.md"
    content = base.b64encode(b"# " + repo_name.encode()).decode()
    data = {
        "message": "Initial commit: add README.md",
        "content": content
    }
    response = requests.put(url, json=data, headers=HEADERS)
    if response.status_code in (201, 200):
        return response.json()
    else:
        print("Failed to create README.md:", response.status_code, response.text)
        return None
    
def clone_repo(repoURL):
    repo_name = repoURL.rstrip('/').split('/')[-1].replace('.git', '')
    result = subprocess.run(["git", "clone", repoURL, repo_name], capture_output=True, text=True)
    if result.returncode == 0:
        return True
    else:
        return False
