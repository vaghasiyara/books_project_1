from fastapi import Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import HTTPException

# Use in-memory storage instead of Redis
limiter = Limiter(
    key_func=get_remote_address,
    storage_uri="memory://",
    enabled=True
)

async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    raise HTTPException(
        status_code=429,
        detail="Rate limit exceeded",
        headers={"Retry-After": str(exc.retry_after)}
    )
