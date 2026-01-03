from __future__ import annotations
from typing import Optional, List, Dict
from app.core.github_client import github_client
from app.config import get_settings
from app.models.keybind import Keybind, Platform
from app.parsers.markdown_keybinds import MarkdownKeybindParser
from app.parsers.skhd_parser import SkhdParser
from app.parsers.hyprland_parser import HyprlandParser

settings = get_settings()

class KeybindService:
    def __init__(self):
        self.md_parser_yabai = MarkdownKeybindParser(platform="yabai")
        self.md_parser_hyprland = MarkdownKeybindParser(platform="hyprland")
        self.skhd_parser = SkhdParser()
        self.hyprland_parser = HyprlandParser()
        self._cache: Dict[str, List[Keybind]] = {}
    
    async def get_keybinds(self, platform: Platform) -> List[Keybind]:
        if platform in self._cache:
            return self._cache[platform]
        
        keybinds = []
        repo = settings.repos.get(platform)
        if not repo:
            return []
        
        if platform == "yabai":
            keybinds = await self._fetch_yabai_keybinds(repo)
        elif platform == "hyprland":
            keybinds = await self._fetch_hyprland_keybinds(repo)
        
        self._cache[platform] = keybinds
        return keybinds
    
    async def _fetch_yabai_keybinds(self, repo: str) -> List[Keybind]:
        keybinds = []
        
        md_content = await github_client.get_raw_file(repo, "Keybinds.md")
        if md_content:
            keybinds.extend(self.md_parser_yabai.parse(md_content))
        
        skhd_content = await github_client.get_raw_file(repo, "skhdrc")
        if skhd_content and not keybinds:
            keybinds.extend(self.skhd_parser.parse(skhd_content))
        
        return keybinds
    
    async def _fetch_hyprland_keybinds(self, repo: str) -> List[Keybind]:
        keybinds = []
        
        md_content = await github_client.get_raw_file(repo, "KEYBINDS.md")
        if md_content:
            keybinds.extend(self.md_parser_hyprland.parse(md_content))
        
        conf_content = await github_client.get_raw_file(repo, "hyprland.conf")
        if conf_content and not keybinds:
            keybinds.extend(self.hyprland_parser.parse(conf_content))
        
        return keybinds
    
    async def get_keybinds_by_category(self, platform: Platform, category: str) -> List[Keybind]:
        keybinds = await self.get_keybinds(platform)
        return [kb for kb in keybinds if kb.category.lower() == category.lower()]
    
    async def get_categories(self, platform: Platform) -> List[str]:
        keybinds = await self.get_keybinds(platform)
        return list(set(kb.category for kb in keybinds))
    
    def clear_cache(self):
        self._cache.clear()

keybind_service = KeybindService()
