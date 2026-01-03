from __future__ import annotations
from typing import Optional, Any, Dict, List
import httpx
from app.config import get_settings

settings = get_settings()

class GitHubClient:
    BASE_URL = "https://api.github.com"
    RAW_URL = "https://raw.githubusercontent.com"
    
    def __init__(self):
        self.headers = {"Accept": "application/vnd.github.v3+json"}
        if settings.github_token:
            self.headers["Authorization"] = f"token {settings.github_token}"
    
    async def get_raw_file(self, repo: str, path: str, branch: str = "main") -> Optional[str]:
        url = f"{self.RAW_URL}/{repo}/{branch}/{path}"
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, headers=self.headers)
            if resp.status_code == 200:
                return resp.text
            return None
    
    async def get_repo_info(self, repo: str) -> Optional[Dict[str, Any]]:
        url = f"{self.BASE_URL}/repos/{repo}"
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, headers=self.headers)
            if resp.status_code == 200:
                return resp.json()
            return None
    
    async def get_repo_contents(self, repo: str, path: str = "", branch: str = "main") -> Optional[List[Dict]]:
        url = f"{self.BASE_URL}/repos/{repo}/contents/{path}"
        params = {"ref": branch}
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, headers=self.headers, params=params)
            if resp.status_code == 200:
                return resp.json()
            return None
    
    async def get_user_repos(self, username: str) -> Optional[List[Dict]]:
        url = f"{self.BASE_URL}/users/{username}/repos"
        params = {"sort": "updated", "per_page": 100}
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, headers=self.headers, params=params)
            if resp.status_code == 200:
                return resp.json()
            return None

github_client = GitHubClient()
