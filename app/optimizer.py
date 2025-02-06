import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import FinancialRecord
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO)

async def optimize_finances(user_id: int, db: AsyncSession):
    """Оптимизирует финансы с ретроспективным анализом и помесячными данными с учетом новых параметров."""

    result = await db.execute(select(FinancialRecord).where(FinancialRecord.user_id == user_id))
    records = result.scalars().all()

    deposits = []
    loans = []

    for record in records:
        if record.end_date and record.start_date and record.end_date < record.start_date:
            logging.warning(f"⚠️ Дата окончания раньше даты начала для {record.type} '{record.bank_name}', запись игнорируется.")
            continue

        # 🔄 Обновление процентной ставки на основе истории изменений
        if record.interest_rate_changes:
            for change in record.interest_rate_changes:
                change_date = datetime.strptime(change["date"], "%Y-%m-%d")
                if change_date < datetime.utcnow():
                    record.interest_rate = change["rate"]

        if record.type == "deposit":
            deposits.append(record)
        elif record.type == "loan":
            loans.append(record)

    logging.info(f"🔍 Найдено депозитов: {len(deposits)}, кредитов: {len(loans)}")
    # ✅ 🔄 Анализ кредитных карт
    for card in credit_cards:
        if card.available_balance and card.available_balance > 0:
            recommendations.append(
                f"💳 У вас доступно {card.available_balance:.2f} ₽ на карте '{card.bank_name}'. "
                "Рассмотрите использование вместо кредита, чтобы избежать процентов."
            )

        if card.grace_period_end_date and card.grace_period_end_date > datetime.utcnow():
            recommendations.append(
                f"⌛ Кредитная карта '{card.bank_name}' в грейс-периоде до {card.grace_period_end_date.strftime('%Y-%m-%d')}. "
                "Оплатите баланс вовремя, чтобы не платить проценты!"
            )

        # 🏦 Проверка кредитного лимита
        if card.credit_limit and card.credit_limit > 0 and card.available_balance < card.credit_limit * 0.3:
            recommendations.append(
                f"⚠️ Осторожно! Кредитная карта '{card.bank_name}' использована более чем на 70% лимита. "
                "Это может снизить ваш кредитный рейтинг."
            )

        # 🔄 Рекомендация по рефинансированию кредитной карты
        if card.refinance_rate and card.refinance_rate < card.purchase_interest_rate:
            recommendations.append(
                f"🔄 Рассмотрите рефинансирование кредитной карты '{card.bank_name}' на ставку {card.refinance_rate:.2f}%, "
                f"так как текущая ставка на покупки {card.purchase_interest_rate:.2f}%."
            )

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
        total_fees = 0
        total_penalties = 0

        while current_date <= datetime.utcnow():
            month = current_date.strftime("%Y-%m")
            
            # Доход с депозита за месяц
            deposit_income = (best_deposit.amount * best_deposit.interest_rate) / 12
            total_deposit_income += deposit_income

            # Переплата по кредиту за месяц
            loan_payment = (worst_loan.amount * worst_loan.interest_rate) / 12
            total_loan_overpayment += loan_payment

            # 💰 Учет комиссий и штрафов
            if best_deposit.fee:
                total_fees += best_deposit.fee / 12  # Комиссия разбивается на месяцы

            if worst_loan.penalty:
                total_penalties += worst_loan.penalty / 12  # Штраф делится на месяцы

            net_savings = deposit_income - loan_payment - (total_fees + total_penalties)

            monthly_report.append({
                "month": month,
                "deposit_income": round(deposit_income, 2),
                "loan_payment": round(loan_payment, 2),
                "fees": round(total_fees, 2),
                "penalties": round(total_penalties, 2),
                "net_savings": round(net_savings, 2)
            })

            current_date += timedelta(days=30)  # Переходим к следующему месяцу

        savings = total_deposit_income - total_loan_overpayment - total_fees - total_penalties

        logging.info(f"📊 Доход с депозита: {total_deposit_income:.2f}")
        logging.info(f"📊 Переплата по кредиту: {total_loan_overpayment:.2f}")
        logging.info(f"💡 Итоговая разница (учитывая комиссии и штрафы): {savings:.2f}")

        retrospective_analysis.append({
            "past_deposit_income": round(total_deposit_income, 2),
            "past_loan_overpayment": round(total_loan_overpayment, 2),
            "total_fees": round(total_fees, 2),
            "total_penalties": round(total_penalties, 2),
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
    # 📊 Улучшенный анализ месячного отчета
    for record in records:
        month = datetime.utcnow().strftime("%Y-%m")
        loan_payment = (record.amount * record.interest_rate) / 12 if record.type == "loan" else 0
        deposit_income = (record.amount * record.interest_rate) / 12 if record.type == "deposit" else 0
        credit_card_fee = record.monthly_fee if record.type == "credit_card" else 0

        monthly_report.append({
            "month": month,
            "deposit_income": round(deposit_income, 2),
            "loan_payment": round(loan_payment, 2),
            "credit_card_fee": round(credit_card_fee, 2),
            "net_balance": round(deposit_income - loan_payment - credit_card_fee, 2)
        })

    # 📉 Анализ долговой нагрузки
    total_loan_expenses = sum((loan.amount * loan.interest_rate) / 12 for loan in loans)
    total_income = sum(deposit.amount * deposit.interest_rate / 12 for deposit in deposits)
    debt_ratio = (total_loan_expenses / (total_income + 1)) * 100  # Чтобы избежать деления на 0

    if debt_ratio > 40:
        recommendations.append(
            f"⚠️ Внимание! Долговая нагрузка {debt_ratio:.1f}%. "
            "Рекомендуется уменьшить платежи по кредитам или увеличить доход."
        )

    logging.info(f"📢 Итоговые рекомендации: {recommendations}")

    return {
        "recommendations": recommendations,
        "retrospective_analysis": retrospective_analysis,
        "monthly_report
::contentReference[oaicite:0]{index=0}
 
