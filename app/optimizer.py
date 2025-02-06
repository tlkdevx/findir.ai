import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import FinancialRecord
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO)


async def optimize_finances(user_id: int, db: AsyncSession):
    """Оптимизирует финансы с ретроспективным анализом и помесячными данными."""

    result = await db.execute(select(FinancialRecord).where(FinancialRecord.user_id == user_id))
    records = result.scalars().all()

    deposits = []
    loans = []

    for record in records:
        if record.end_date and record.start_date and record.end_date < record.start_date:
            logging.warning(f"⚠️ Дата окончания раньше даты начала для {record.type} '{record.bank_name}', запись игнорируется.")
            continue

        if record.type == "deposit":
            deposits.append(record)
        elif record.type == "loan":
            loans.append(record)

    logging.info(f"🔍 Найдено депозитов: {len(deposits)}, кредитов: {len(loans)}")

    if not deposits or not loans:
        logging.info("❌ Нет депозитов или кредитов — нечего анализировать.")
        return {"recommendations": [], "monthly_report": []}

    # Выбираем лучший депозит
    best_deposit = max(deposits, key=lambda d: d.amount * (1 + d.interest_rate * ((d.end_date - d.start_date).days / 365)), default=None)

    # Выбираем самый дорогой кредит
    worst_loan = max(loans, key=lambda l: l.amount * (1 + l.interest_rate * ((l.end_date - l.start_date).days / 365)), default=None)

    logging.info(f"💰 Лучший депозит: {best_deposit}")
    logging.info(f"💸 Худший кредит: {worst_loan}")

    recommendations = []
    retrospective_analysis = []
    monthly_report = []

    if best_deposit and worst_loan:
        logging.info(f"🔍 Анализируем ретроспективно...")

        retrospective_start = datetime.utcnow() - timedelta(days=365)  # Анализируем за последний год
        current_date = retrospective_start

        total_deposit_income = 0
        total_loan_overpayment = 0

        while current_date <= datetime.utcnow():
            month = current_date.strftime("%Y-%m")
            
            # Доход с депозита за месяц
            deposit_income = (best_deposit.amount * best_deposit.interest_rate) / 12
            total_deposit_income += deposit_income

            # Переплата по кредиту за месяц
            loan_payment = (worst_loan.amount * worst_loan.interest_rate) / 12
            total_loan_overpayment += loan_payment

            monthly_report.append({
                "month": month,
                "deposit_income": round(deposit_income, 2),
                "loan_payment": round(loan_payment, 2),
                "net_savings": round(deposit_income - loan_payment, 2)
            })

            current_date += timedelta(days=30)  # Переходим к следующему месяцу

        savings = total_deposit_income - total_loan_overpayment

        logging.info(f"📊 Доход с депозита: {total_deposit_income:.2f}")
        logging.info(f"📊 Переплата по кредиту: {total_loan_overpayment:.2f}")
        logging.info(f"💡 Итоговая разница: {savings:.2f}")

        retrospective_analysis.append({
            "past_deposit_income": round(total_deposit_income, 2),
            "past_loan_overpayment": round(total_loan_overpayment, 2),
            "potential_savings": round(savings, 2),
            "start_date": retrospective_start.strftime("%Y-%m-%d"),
            "end_date": datetime.utcnow().strftime("%Y-%m-%d")
        })

        if savings > 0:
            recommendations.append(f"✅ Закройте кредит '{worst_loan.bank_name}' за счет депозита '{best_deposit.bank_name}'. Экономия: {savings:.2f}")
        else:
            logging.info("⚠️ Полное закрытие кредита невыгодно, проверяем частичное погашение...")

            partial_payment = best_deposit.amount * 0.3  # Используем 30% депозита на частичное погашение
            new_loan_amount = worst_loan.amount - partial_payment
            new_loan_cost = new_loan_amount * (1 + worst_loan.interest_rate * ((worst_loan.end_date - worst_loan.start_date).days / 365))
            partial_savings = total_loan_overpayment - new_loan_cost

            if partial_savings > 0:
                recommendations.append(f"💳 Рассмотрите частичное погашение кредита '{worst_loan.bank_name}' на сумму {partial_payment:.2f}. Это уменьшит переплату на {partial_savings:.2f}.")
            else:
                logging.info("⚠️ Частичное погашение не дает выгоды.")

    # Проверяем возможность рефинансирования
    for loan in loans:
        if loan.refinance_available:
            recommendations.append(f"🔄 Рассмотрите рефинансирование кредита '{loan.bank_name}', так как банк предлагает лучшие условия.")

    logging.info(f"📢 Итоговые рекомендации: {recommendations}")

    return {
        "recommendations": recommendations,
        "retrospective_analysis": retrospective_analysis,
        "monthly_report": monthly_report
    }
