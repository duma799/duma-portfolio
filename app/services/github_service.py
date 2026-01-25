from __future__ import annotations

from typing import Dict, List, Optional

from app.config import get_settings
from app.core.github_client import github_client
from app.models.keybind import ChangelogEntry, RepoInfo

settings = get_settings()


class GitHubService:
    async def get_repo_stats(self, repo: str) -> Optional[RepoInfo]:
        info = await github_client.get_repo_info(repo)
        if not info:
            return None

        return RepoInfo(
            name=info.get("name", ""),
            full_name=info.get("full_name", ""),
            description=info.get("description"),
            stars=info.get("stargazers_count", 0),
            forks=info.get("forks_count", 0),
            language=info.get("language"),
            url=info.get("html_url", ""),
            topics=info.get("topics", []),
        )

    async def get_all_repos(self) -> List[RepoInfo]:
        repos = await github_client.get_user_repos(settings.github_username)
        if not repos:
            return []

        return [
            RepoInfo(
                name=r.get("name", ""),
                full_name=r.get("full_name", ""),
                description=r.get("description"),
                stars=r.get("stargazers_count", 0),
                forks=r.get("forks_count", 0),
                language=r.get("language"),
                url=r.get("html_url", ""),
                topics=r.get("topics", []),
            )
            for r in repos
            if not r.get("fork")
        ]

    async def get_dotfiles_repos(self) -> Dict[str, RepoInfo]:
        result = {}
        for platform, repo in settings.repos.items():
            info = await self.get_repo_stats(repo)
            if info:
                result[platform] = info
        return result

    async def get_readme(self, platform: str) -> Optional[str]:
        repo = settings.repos.get(platform)
        if not repo:
            return None
        return await github_client.get_readme(repo)

    async def get_changelog(self, repo: str) -> List[ChangelogEntry]:
        # Try releases first
        releases = await github_client.get_releases(repo)
        if releases:
            return [
                ChangelogEntry(
                    version=r.get("tag_name"),
                    title=r.get("name") or r.get("tag_name", "Release"),
                    body=r.get("body"),
                    date=r.get("published_at", "")[:10],
                    url=r.get("html_url", ""),
                    type="release",
                )
                for r in releases
            ]

        # Fall back to commits
        commits = await github_client.get_commits(repo)
        if commits:
            return [
                ChangelogEntry(
                    title=c.get("commit", {}).get("message", "").split("\n")[0],
                    body="\n".join(c.get("commit", {}).get("message", "").split("\n")[1:]).strip()
                    or None,
                    date=c.get("commit", {}).get("author", {}).get("date", "")[:10],
                    url=c.get("html_url", ""),
                    type="commit",
                )
                for c in commits
            ]

        return []


github_service = GitHubService()
