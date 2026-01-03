from __future__ import annotations
from typing import List
from abc import ABC, abstractmethod
from app.models.keybind import Keybind

class BaseKeybindParser(ABC):
    @abstractmethod
    def parse(self, content: str) -> List[Keybind]:
        pass
    
    def normalize_modifier(self, mod: str) -> str:
        mod = mod.lower().strip()
        mappings = {
            "alt": "opt", "option": "opt", "lalt": "opt", "ralt": "opt",
            "ctrl": "ctrl", "control": "ctrl", "lctrl": "ctrl", "rctrl": "ctrl",
            "shift": "shift", "lshift": "shift", "rshift": "shift",
            "cmd": "cmd", "super": "cmd", "mod4": "cmd", "command": "cmd",
            "$mainmod": "cmd", "mainmod": "cmd",
        }
        return mappings.get(mod, mod)
    
    def normalize_key(self, key: str) -> str:
        key = key.lower().strip()
        mappings = {
            "return": "enter", "escape": "esc", "space": "space",
            "left": "left", "right": "right", "up": "up", "down": "down",
            "backspace": "backspace", "tab": "tab", "delete": "del",
        }
        return mappings.get(key, key)
