import os

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

import app.core.config as app_config
from app.api.routes import api_router

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

if app_config.DEVELOPER_MODE:
    app = FastAPI(title=app_config.PROJECT_NAME)
else:
    app = FastAPI(title=app_config.PROJECT_NAME, openapi_url=None, redoc_url=None, docs_url=None)

app.mount("/dist", StaticFiles(directory=os.path.join(APP_ROOT, "dist")), name="dist")
templates = Jinja2Templates(directory=os.path.join(APP_ROOT, "dist"))

if app_config.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in app_config.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=app_config.ALLOW_METHODS,
        allow_headers=app_config.ALLOW_HEADERS,
    )

APP_ROOT = os.path.dirname(os.path.abspath(__file__))


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.exception_handler(404)
def not_found(request, exc):
    return RedirectResponse("/")


app.include_router(api_router, prefix=app_config.API_PATH)
