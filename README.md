# Duma Portfolio

A Python-powered portfolio website showcasing my dotfiles configurations for Hyprland (Linux) and Yabai (macOS).

## Features

- **Interactive Keyboard Visualizer** - Visual keybinding display with hover interactions
- **Live GitHub Parsing** - Keybinds parsed directly from repositories
- **Config Browser** - View config files with syntax highlighting
- **Wallpaper Gallery** - Screenshots and wallpapers showcase
- **Responsive Design** - Works on all devices

## Tech Stack

- **Backend**: FastAPI, Pydantic, httpx
- **Frontend**: Jinja2, HTMX, Alpine.js, Tailwind CSS
- **Syntax Highlighting**: Pygments

## Setup

1. Install dependencies:
   ```bash
   pip install -e .
   # or with uv
   uv pip install -e .
   ```

2. Copy environment file:
   ```bash
   cp .env.example .env
   ```

3. Run the development server:
   ```bash
   uvicorn app.main:app --reload
   ```

4. Open http://localhost:8000

## Project Structure

```
duma-portfolio/
├── app/
│   ├── api/routes/      # API endpoints
│   ├── core/            # GitHub client, caching
│   ├── models/          # Pydantic models
│   ├── parsers/         # Keybind parsers (md, skhd, hyprland)
│   ├── services/        # Business logic
│   └── templates/       # Jinja2 templates
├── static/              # CSS, JS, images
├── scripts/             # CLI utilities
└── tests/               # Test suite
```

## API Endpoints

- `GET /api/keybinds/{platform}` - Get keybinds for platform
- `GET /api/configs/{repo}/file/{path}` - Get highlighted config file
- `GET /api/github/repos` - Get all repositories
- `GET /api/github/dotfiles` - Get dotfiles repositories info

## License

MIT
