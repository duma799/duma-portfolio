from __future__ import annotations

import re
from typing import Any, Dict, List, Optional

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

    async def get_repo_contents(
        self, repo: str, path: str = "", branch: str = "main"
    ) -> Optional[List[Dict]]:
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

    async def get_readme(self, repo: str) -> Optional[str]:
        for branch in ["main", "master"]:
            content = await self.get_raw_file(repo, "README.md", branch)
            if content:
                return self._fix_relative_urls(content, repo, branch)
        return None

    async def get_releases(self, repo: str, per_page: int = 10) -> Optional[List[Dict]]:
        url = f"{self.BASE_URL}/repos/{repo}/releases"
        params = {"per_page": per_page}
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, headers=self.headers, params=params)
            if resp.status_code == 200:
                return resp.json()
            return None

    async def get_commits(self, repo: str, per_page: int = 10) -> Optional[List[Dict]]:
        url = f"{self.BASE_URL}/repos/{repo}/commits"
        params = {"per_page": per_page}
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, headers=self.headers, params=params)
            if resp.status_code == 200:
                return resp.json()
            return None

    def _fix_relative_urls(self, content: str, repo: str, branch: str) -> str:
        raw_base = f"{self.RAW_URL}/{repo}/{branch}"

        # fix markdown images
        def replace_md_image(match):
            alt = match.group(1)
            path = match.group(2)
            if path.startswith(("http://", "https://", "//")):
                return match.group(0)
            path = path.lstrip("./")
            return f"![{alt}]({raw_base}/{path})"

        content = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", replace_md_image, content)

        # fix html img tags
        def replace_html_img(match):
            prefix = match.group(1)
            path = match.group(2)
            if path.startswith(("http://", "https://", "//")):
                return match.group(0)
            path = path.lstrip("./")
            return f'{prefix}"{raw_base}/{path}"'

        content = re.sub(r'(<img[^>]*src=)"([^"]+)"', replace_html_img, content)

        return content


github_client = GitHubClient()
