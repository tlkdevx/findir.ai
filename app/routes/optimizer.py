from fastapi import APIRouter, Query

router = APIRouter()

@router.get("/api/optimize")
async def optimize_finances(user_id: int = Query(...)):
    return [
        {
            "id": 1,
            "message": "Рефинансируйте кредит в другом банке под 10%",
            "current_outcome": 120000,
            "optimized_outcome": 115000
        },
        {
            "id": 2,
            "message": "Переложите 50 000 ₽ с депозита под 5% на вклад под 7%",
            "current_outcome": 105000,
            "optimized_outcome": 110000
        },
        {
            "id": 3,
            "message": "Закройте кредит на 15000 ₽ досрочно, чтобы сэкономить 5000 ₽ на процентах",
            "current_outcome": 95000,
            "optimized_outcome": 100000
        }
    ]
