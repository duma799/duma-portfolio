from __future__ import annotations
from typing import Optional, List
from app.parsers.base import BaseKeybindParser
from app.models.keybind import Keybind

class SkhdParser(BaseKeybindParser):
    def __init__(self):
        self.platform = "yabai"
    
    def parse(self, content: str) -> List[Keybind]:
        keybinds = []
        current_category = "General"
        
        for line in content.split(chr(10)):
            line = line.strip()
            if not line:
                continue
            if line.startswith("#") and not line.startswith("#!/"):
                category = line.lstrip("#").strip()
                if category and not category.startswith("!"):
                    current_category = category
                continue
            if " : " in line and not line.startswith("#"):
                keybind = self.parse_skhd_line(line, current_category)
                if keybind:
                    keybinds.append(keybind)
        return keybinds
    
    def parse_skhd_line(self, line: str, category: str) -> Optional[Keybind]:
        try:
            hotkey_part, command = line.split(" : ", 1)
            hotkey_part = hotkey_part.strip()
            command = command.strip()
            if " - " in hotkey_part:
                mod_part, key = hotkey_part.rsplit(" - ", 1)
            else:
                return None
            modifiers = []
            for mod in mod_part.split("+"):
                mod = mod.strip()
                if mod:
                    modifiers.append(self.normalize_modifier(mod))
            key = self.normalize_key(key.strip())
            action = self.command_to_action(command)
            return Keybind(
                platform=self.platform,
                category=category,
                modifiers=modifiers,
                key=key,
                action=action,
                command=command,
            )
        except ValueError:
            return None
    
    def command_to_action(self, cmd: str) -> str:
        if "open -a" in cmd:
            app = cmd.split("open -a")[-1].strip().strip(chr(34))
            return f"Open {app}"
        elif "yabai -m window --focus" in cmd:
            direction = cmd.split("--focus")[-1].strip()
            return f"Focus window {direction}"
        elif "yabai -m window --swap" in cmd:
            direction = cmd.split("--swap")[-1].strip()
            return f"Swap window {direction}"
        elif "yabai -m window --resize" in cmd:
            return "Resize window"
        elif "yabai -m window --toggle" in cmd:
            toggle = cmd.split("--toggle")[-1].strip()
            return f"Toggle {toggle}"
        elif "yabai -m space --layout" in cmd:
            layout = cmd.split("--layout")[-1].strip()
            return f"Set {layout} layout"
        elif "yabai -m space --rotate" in cmd:
            return "Rotate layout"
        elif "yabai -m space --balance" in cmd:
            return "Balance windows"
        elif "yabai --restart-service" in cmd:
            return "Restart yabai"
        return cmd[:50] + "..." if len(cmd) > 50 else cmd
