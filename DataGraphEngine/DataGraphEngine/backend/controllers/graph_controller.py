"""
Graph controller — request/response handling.
"""
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from backend.services.analytics_service import analyze, natural_language_query


async def handle_analyze(body: dict) -> JSONResponse:
    try:
        result = analyze(body)
        return JSONResponse(content=result)
    except KeyError as e:
        raise HTTPException(400, detail=f"Missing field: {e}")
    except Exception as e:
        raise HTTPException(500, detail=str(e))


async def handle_query(body: dict) -> JSONResponse:
    try:
        result = natural_language_query(body)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(500, detail=str(e))
