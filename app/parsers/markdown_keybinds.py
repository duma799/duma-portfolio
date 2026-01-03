from __future__ import annotations
from typing import Optional, List
from app.parsers.base import BaseKeybindParser
from app.models.keybind import Keybind

class MarkdownKeybindParser(BaseKeybindParser):
    def __init__(self, platform: str = "yabai"):
        self.platform = platform
        self.current_category = "General"
    
    def parse(self, content: str) -> List[Keybind]:
        keybinds = []
        lines = content.split(chr(10))
        
        for line in lines:
            line = line.strip()
            
            if line.startswith("## "):
                self.current_category = line[3:].strip()
                continue
            
            if line.startswith("|") and "---" not in line:
                parts = [p.strip() for p in line.split("|")[1:-1]]
                if len(parts) >= 2 and parts[0].lower() != "keybind":
                    keybind = self.parse_keybind_cell(parts[0], parts[1])
                    if keybind:
                        keybinds.append(keybind)
        
        return keybinds
    
    def parse_keybind_cell(self, keybind_str: str, action: str) -> Optional[Keybind]:
        keybind_str = keybind_str.strip()
        if not keybind_str:
            return None
        
        parts = [p.strip() for p in keybind_str.split("+")]
        if not parts:
            return None
        
        modifiers = []
        key = ""
        
        for part in parts:
            part_lower = part.lower()
            if part_lower in ["option", "opt", "alt", "ctrl", "control", "shift", "cmd", "command"]:
                modifiers.append(self.normalize_modifier(part))
            elif part_lower == "arrow":
                key = "arrows"
            else:
                key = self.normalize_key(part.split("/")[0])
        
        if not key:
            return None
        
        return Keybind(
            platform=self.platform,
            category=self.current_category,
            modifiers=modifiers,
            key=key,
            action=action,
        )
