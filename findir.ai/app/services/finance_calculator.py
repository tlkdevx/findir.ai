from datetime import datetime, timedelta
from typing import List, Dict

def calculate_future_scenarios(financial_data: List[Dict], months_list=[1, 6, 12]):
    """
    Прогнозирует движение денежных средств на 1, 6 и 12 месяцев вперед.
    
    :param financial_data: список словарей с данными о кредитах и вкладах
    :param months_list: периоды, на которые нужно рассчитать прогноз
    :return: словарь с прогнозами на указанные месяцы
    """
    today = datetime.today()
    scenarios = {}

    for months in months_list:
        future_date = today + timedelta(days=months * 30)
        total_loan_remaining = 0  # Общий остаток по кредитам
        total_deposit_balance = 0  # Общий баланс по вкладам
        total_interest_earned = 0  # Проценты по вкладам

        for record in financial_data:
            if record["type"] == "loan":
                # Рассчитываем остаток по кредиту через X месяцев
                interest_rate = record["interest_rate"] / 100 / 12  # Месячная ставка
                months_remaining = (record["end_date"] - today).days // 30
                if months_remaining > months:
                    total_loan_remaining += record["balance"] * (1 + interest_rate) ** months - record["monthly_payment"] * months
                else:
                    total_loan_remaining += max(0, record["balance"] - record["monthly_payment"] * months_remaining)

            elif record["type"] == "deposit":
                # Рассчитываем проценты по вкладу через X месяцев
                interest_rate = record["interest_rate"] / 100 / 12  # Месячная ставка
                deposit_growth = record["balance"] * (1 + interest_rate) ** months
                total_interest_earned += deposit_growth - record["balance"]
                total_deposit_balance += deposit_growth

        scenarios[f"{months}_months"] = {
            "loan_remaining": round(total_loan_remaining, 2),
            "deposit_balance": round(total_deposit_balance, 2),
            "interest_earned": round(total_interest_earned, 2),
            "date": future_date.strftime("%Y-%m-%d")
        }

    return scenarios
