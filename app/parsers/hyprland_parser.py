from __future__ import annotations

from typing import Dict, List, Optional

from app.models.keybind import Keybind
from app.parsers.base import BaseKeybindParser


class HyprlandParser(BaseKeybindParser):
    def __init__(self):
        self.platform = "hyprland"
        self.variables: Dict[str, str] = {}

    def parse(self, content: str) -> List[Keybind]:
        keybinds = []
        current_category = "General"

        for line in content.split("\n"):
            line = line.strip()
            if not line or line.startswith("#"):
                if line.startswith("#"):
                    cat = line.lstrip("#").strip()
                    if cat and len(cat) < 30:
                        current_category = cat
                continue

            if line.startswith("$") and "=" in line:
                var_name, var_value = line.split("=", 1)
                self.variables[var_name.strip()] = var_value.strip()
                continue

            if line.startswith("bind"):
                keybind = self.parse_bind_line(line, current_category)
                if keybind:
                    keybinds.append(keybind)

        return keybinds

    def parse_bind_line(self, line: str, category: str) -> Optional[Keybind]:
        try:
            _, rest = line.split("=", 1)
            parts = [p.strip() for p in rest.split(",")]
            if len(parts) < 3:
                return None

            mods_str = parts[0]
            key = parts[1]
            dispatcher = parts[2]
            params = ",".join(parts[3:]) if len(parts) > 3 else ""

            mods_str = self.expand_variables(mods_str)
            modifiers = []
            for mod in mods_str.split():
                mod = mod.strip()
                if mod:
                    modifiers.append(self.normalize_modifier(mod))

            key = self.normalize_key(key)
            action = self.dispatcher_to_action(dispatcher, params)
            command = f"{dispatcher}, {params}" if params else dispatcher

            return Keybind(
                platform=self.platform,
                category=category,
                modifiers=modifiers,
                key=key,
                action=action,
                command=command,
            )
        except (ValueError, IndexError):
            return None

    def expand_variables(self, text: str) -> str:
        for var, value in self.variables.items():
            text = text.replace(var, value)
        return text

    def dispatcher_to_action(self, dispatcher: str, params: str) -> str:
        actions = {
            "exec": f"Run {params.split()[0]}" if params else "Execute",
            "killactive": "Close window",
            "movefocus": f"Focus {params}",
            "movewindow": f"Move window {params}",
            "resizeactive": "Resize window",
            "togglefloating": "Toggle floating",
            "fullscreen": "Toggle fullscreen",
            "workspace": f"Go to workspace {params}",
            "movetoworkspace": f"Move to workspace {params}",
            "togglesplit": "Toggle split",
        }
        return actions.get(dispatcher, f"{dispatcher} {params}".strip())
