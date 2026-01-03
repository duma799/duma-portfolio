from fastapi import APIRouter
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
