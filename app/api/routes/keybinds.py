from __future__ import annotations
from typing import List
from fastapi import APIRouter, HTTPException
from app.services.keybind_service import keybind_service
from app.models.keybind import Keybind, Platform

router = APIRouter()

@router.get("/{platform}", response_model=List[Keybind])
async def get_keybinds(platform: Platform):
    keybinds = await keybind_service.get_keybinds(platform)
    if not keybinds:
        raise HTTPException(status_code=404, detail=f"No keybinds found for {platform}")
    return keybinds

@router.get("/{platform}/categories")
async def get_categories(platform: Platform) -> List[str]:
    return await keybind_service.get_categories(platform)

@router.get("/{platform}/category/{category}", response_model=List[Keybind])
async def get_keybinds_by_category(platform: Platform, category: str):
    return await keybind_service.get_keybinds_by_category(platform, category)

@router.post("/refresh")
async def refresh_cache():
    keybind_service.clear_cache()
    return {"status": "cache cleared"}
