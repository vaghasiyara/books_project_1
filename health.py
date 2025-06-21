from fastapi import APIRouter
from fastapi.responses import JSONResponse
import redis
import os

router = APIRouter()

@router.get("/health")
async def health_check():
    return {"status": "ok"}

@router.get("/health/redis")
async def redis_health_check():
    try:
        r = redis.Redis(host='localhost', port=6379)
        return {"redis": "connected" if r.ping() else "disconnected"}
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={"redis": "unavailable", "error": str(e)}
        )
