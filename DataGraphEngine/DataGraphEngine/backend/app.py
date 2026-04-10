"""
DataGraphEngine — FastAPI backend
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import uvicorn

from backend.routes.graph_routes import router as graph_router

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

app = FastAPI(title="DataGraphEngine", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(graph_router, prefix="/api/graph")

app.mount(
    "/static",
    StaticFiles(directory=os.path.join(BASE_DIR, "frontend", "static")),
    name="static",
)

templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "frontend", "templates"))

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

if __name__ == "__main__":
    uvicorn.run("backend.app:app", host="0.0.0.0", port=8000, reload=True)
