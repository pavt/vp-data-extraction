import requests
import json
from typing import Dict, Optional

class GitHubAPI:
    def __init__(self, token: str, rate_limit_pause: float = 0.5):
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github.v3+json",
            "X-GitHub-Api-Version": "2022-11-28"
        }
        self.rate_limit_pause = rate_limit_pause

    def get_json(self, url: str) -> Optional[Dict]:
        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"Error obteniendo datos de {url}: {e}")
        return None
