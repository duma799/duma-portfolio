from __future__ import annotations

from typing import List, Literal, Optional

from pydantic import BaseModel

Platform = Literal["hyprland", "yabai"]


class Keybind(BaseModel):
    platform: Platform
    category: str
    modifiers: List[str]
    key: str
    action: str
    command: Optional[str] = None


class KeyMapping(BaseModel):
    key_code: str
    display: str
    row: int
    position: int
    width: float = 1.0
    is_modifier: bool = False
    keybinds: List[Keybind] = []


class KeyboardLayout(BaseModel):
    platform: Platform
    rows: List[List[KeyMapping]]


class ConfigFile(BaseModel):
    repo: str
    path: str
    content: str
    highlighted_html: str
    language: str


class RepoInfo(BaseModel):
    name: str
    full_name: str
    description: Optional[str]
    stars: int
    forks: int
    language: Optional[str]
    url: str
    topics: List[str] = []


class ChangelogEntry(BaseModel):
    version: Optional[str] = None
    title: str
    body: Optional[str] = None
    date: str
    url: str
    type: Literal["release", "commit"]
