from fastapi import APIRouter, HTTPException
from app.services.config_service import config_service

router = APIRouter()

@router.get("/{repo:path}/file/{file_path:path}")
async def get_config_file(repo: str, file_path: str):
    config = await config_service.get_config_file(repo, file_path)
    if not config:
        raise HTTPException(status_code=404, detail="Config file not found")
    return config

@router.get("/highlight-css")
async def get_highlight_css():
    return {"css": config_service.get_highlight_css()}
