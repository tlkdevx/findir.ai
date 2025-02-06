from fastapi import APIRouter
from ..services.finance_calculator import calculate_future_scenarios

router = APIRouter()

@router.get("/recommendations")
async def get_recommendations():
    """
    Возвращает финансовые рекомендации, включая прогноз на 1/6/12 месяцев.
    """
    # Заглушка - пример финансовых данных, замените на реальное получение из БД
    financial_data = [
        {"type": "loan", "balance": 100000, "interest_rate": 10, "monthly_payment": 5000, "end_date": datetime(2027, 1, 1)},
        {"type": "deposit", "balance": 50000, "interest_rate": 5, "end_date": datetime(2030, 1, 1)}
    ]

    future_scenarios = calculate_future_scenarios(financial_data)

    return {"scenarios": future_scenarios}
