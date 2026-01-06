from fastapi import APIRouter, HTTPException

from app.services.github_service import github_service

router = APIRouter()


@router.get("/repos")
async def get_all_repos():
    return await github_service.get_all_repos()


@router.get("/dotfiles")
async def get_dotfiles_repos():
    return await github_service.get_dotfiles_repos()


@router.get("/repo/{repo:path}")
async def get_repo_info(repo: str):
    return await github_service.get_repo_stats(repo)


@router.get("/readme/{platform}")
async def get_readme(platform: str):
    readme = await github_service.get_readme(platform)
    if not readme:
        raise HTTPException(status_code=404, detail=f"README not found for {platform}")
    return {"content": readme}
