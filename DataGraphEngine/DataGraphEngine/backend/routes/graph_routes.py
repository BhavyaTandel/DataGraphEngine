"""
Graph API routes.
"""
from fastapi import APIRouter, Request
from backend.controllers.graph_controller import handle_analyze, handle_query

router = APIRouter()

@router.post("/analyze")
async def analyze(request: Request):
    body = await request.json()
    return await handle_analyze(body)

@router.post("/query")
async def query(request: Request):
    body = await request.json()
    return await handle_query(body)

@router.get("/ping")
async def ping():
    return {"status": "ok", "service": "DataGraphEngine v2"}
