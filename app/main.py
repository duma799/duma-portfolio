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
