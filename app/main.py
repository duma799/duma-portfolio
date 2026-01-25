import os
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.api.routes import configs, github, keybinds
from app.config import get_settings

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    Path("data").mkdir(exist_ok=True)
    yield


app = FastAPI(
    title=settings.app_name,
    lifespan=lifespan,
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="app/templates")

app.include_router(keybinds.router, prefix="/api/keybinds", tags=["keybinds"])
app.include_router(configs.router, prefix="/api/configs", tags=["configs"])
app.include_router(github.router, prefix="/api/github", tags=["github"])


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "title": "Home"})


@app.get("/about")
async def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request, "title": "About"})


@app.get("/projects")
async def projects(request: Request):
    return templates.TemplateResponse("projects.html", {"request": request, "title": "Projects"})


@app.get("/dotfiles")
async def dotfiles(request: Request):
    return templates.TemplateResponse(
        "dotfiles/index.html", {"request": request, "title": "Dotfiles"}
    )


@app.get("/dotfiles/keybinds")
async def keybinds_page(request: Request):
    return templates.TemplateResponse(
        "dotfiles/keybinds.html", {"request": request, "title": "Keybinds"}
    )


@app.get("/dotfiles/configs")
async def configs_page(request: Request):
    return templates.TemplateResponse(
        "dotfiles/configs.html", {"request": request, "title": "Configs"}
    )


@app.get("/dotfiles/{platform}")
async def platform_page(request: Request, platform: str):
    platform_titles = {
        "yabai": "Yabai (macOS)",
        "hyprland": "Hyprland (Linux)",
    }
    title = platform_titles.get(platform, platform.capitalize())
    return templates.TemplateResponse(
        "dotfiles/platform.html", {"request": request, "title": title, "platform": platform}
    )


@app.get("/gallery")
async def gallery(request: Request):
    gallery_dir = Path("static/images/gallery")
    images = []

    if gallery_dir.exists():
        for file in sorted(gallery_dir.iterdir(), key=lambda x: x.stat().st_mtime, reverse=True):
            if file.suffix.lower() in [".png", ".jpg", ".jpeg", ".webp", ".gif", ".mp4"]:
                # filename format: platform_title_description.ext
                name_parts = file.stem.split("_")
                platform = name_parts[0] if len(name_parts) > 0 else "other"
                title = (
                    name_parts[1].replace("-", " ").title() if len(name_parts) > 1 else file.stem
                )
                description = (
                    name_parts[2].replace("-", " ").capitalize() if len(name_parts) > 2 else ""
                )

                images.append(
                    {
                        "url": f"/static/images/gallery/{file.name}",
                        "title": title,
                        "description": description,
                        "platform": platform.lower(),
                        "is_video": file.suffix.lower() == ".mp4",
                    }
                )

    return templates.TemplateResponse(
        "gallery.html", {"request": request, "title": "Gallery", "images": images}
    )
