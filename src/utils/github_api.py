import requests

from core.config import settings


GITHUB_API_URL = "https://api.github.com"

headers = {
    "Authorization": f"Bearer {settings.GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}


def fetch_repos(owner):
    url = f"{GITHUB_API_URL}/users/{owner}/repos"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.json()}")
        return None
