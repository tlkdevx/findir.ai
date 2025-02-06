from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.optimizer import optimize_finances


router = APIRouter()

@router.get("/api/optimize")
async def optimize_finances(user_id: int = Query(...)):
    return [
        {"id": 1, "message": f"Рефинансируйте кредит, user_id={user_id}"},
        {"id": 2, "message": "Переложите 50 000 ₽ с депозита под 5% на вклад под 7%"},
        {"id": 3, "message": "Закройте кредит на 15000 ₽ досрочно, чтобы сэкономить 5000 ₽ на процентах"},
    ]
