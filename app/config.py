from __future__ import annotations
from functools import lru_cache
from pathlib import Path
from typing import Optional, Dict
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Duma Portfolio"
    debug: bool = False
    github_token: Optional[str] = None
    github_username: str = "duma799"
    github_cache_ttl: int = 3600

    repos: Dict[str, str] = {
        "hyprland": "duma799/hyprduma-config",
        "yabai": "duma799/yabaduma-config",
    }

    base_dir: Path = Path(__file__).parent.parent
    data_dir: Path = base_dir / "data"
    static_dir: Path = base_dir / "static"
    templates_dir: Path = base_dir / "app" / "templates"
    database_url: str = "sqlite+aiosqlite:///data/portfolio.db"

@lru_cache
def get_settings() -> Settings:
    return Settings()
