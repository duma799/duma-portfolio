from __future__ import annotations
from typing import Optional
from pygments import highlight
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.formatters import HtmlFormatter

from app.core.github_client import github_client
from app.models.keybind import ConfigFile

class ConfigService:
    LANGUAGE_MAP = {
        ".py": "python",
        ".sh": "bash",
        ".conf": "ini",
        ".toml": "toml",
        ".yaml": "yaml",
        ".yml": "yaml",
        ".json": "json",
        ".md": "markdown",
        ".lua": "lua",
    }
    
    async def get_config_file(self, repo: str, path: str) -> Optional[ConfigFile]:
        content = await github_client.get_raw_file(repo, path)
        if not content:
            return None
        
        ext = "." + path.split(".")[-1] if "." in path else ""
        language = self.LANGUAGE_MAP.get(ext, "text")
        
        if path.endswith("rc") or path in ["yabairc", "skhdrc", "bordersrc"]:
            language = "bash"
        elif "hyprland" in path:
            language = "ini"
        
        highlighted = self.highlight_code(content, language)
        
        return ConfigFile(
            repo=repo,
            path=path,
            content=content,
            highlighted_html=highlighted,
            language=language,
        )
    
    def highlight_code(self, code: str, language: str) -> str:
        try:
            lexer = get_lexer_by_name(language)
        except:
            lexer = guess_lexer(code)
        
        formatter = HtmlFormatter(
            style="monokai",
            linenos=True,
            cssclass="highlight",
        )
        return highlight(code, lexer, formatter)
    
    def get_highlight_css(self) -> str:
        return HtmlFormatter(style="monokai").get_style_defs(".highlight")

config_service = ConfigService()
