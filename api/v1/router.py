from fastapi import APIRouter, Depends, HTTPException
from auth import get_current_user

router = APIRouter(
    prefix="/api/v1",
    tags=["v1"],
    dependencies=[Depends(get_current_user)]  # Protects all routes in this router
)

@router.get("/protected-route")
async def protected_route(current_user: dict = Depends(get_current_user)):
    return {"message": "You have access to protected route", "user": current_user["username"]}
