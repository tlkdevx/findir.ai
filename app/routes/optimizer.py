from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.optimizer import optimize_finances

router = APIRouter()

@router.get("/optimize")
async def optimize_finances_endpoint(
    user_id: int = Query(..., description="ID пользователя"), 
    db: AsyncSession = Depends(get_db)
):
    return await optimize_finances(user_id, db)
