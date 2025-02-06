from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

# ====== Модель пользователя ======
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    financial_records = relationship("FinancialRecord", back_populates="user", cascade="all, delete")

# ====== Модель финансовых данных ======
class FinancialRecord(Base):
    __tablename__ = "financial_records"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    type = Column(String, nullable=False)  # loan / deposit / credit_card
    bank_name = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    interest_rate = Column(Float, nullable=False)
    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime, nullable=True)  # Может быть пустым для бессрочного депозита
    is_open_ended = Column(Boolean, default=False)  # Бессрочный депозит

    # Ограничения по суммам
    min_amount = Column(Float, nullable=True)  
    max_amount = Column(Float, nullable=True)  

    # Депозиты: разные модели начисления процентов
    interest_accrual_type = Column(String, nullable=True)  # monthly_fixed_date / daily / floating
    future_date = Column(DateTime, nullable=True)  # Дата моделирования будущего состояния депозита

    # Кредиты: график платежей, штрафы
    payment_type = Column(String, nullable=True)  # annuity / differentiated
    payment_day = Column(Integer, nullable=True)  # День месяца для списания платежей
    early_repayment_fee = Column(Boolean, default=False)  # Штраф за досрочное погашение
    refinance_available = Column(Boolean, default=False)  # Доступно ли рефинансирование

    # Кредитные карты
    credit_limit = Column(Float, nullable=True)  
    available_balance = Column(Float, nullable=True)
    grace_period_end_date = Column(DateTime, nullable=True)
    purchase_interest_rate = Column(Float, nullable=True)
    cash_withdrawal_rate = Column(Float, nullable=True)
    refinance_rate = Column(Float, nullable=True)

    # Новые параметры из банковских документов
    monthly_fee = Column(Float, nullable=True)  # Ежемесячная комиссия
    cashback_percent = Column(Float, nullable=True)  # Процент кэшбэка
    overdraft_available = Column(Boolean, default=False)  # Возможность овердрафта
    overdraft_limit = Column(Float, nullable=True)  # Лимит овердрафта

    # Новые параметры для расширенного анализа
    liquidity_check = Column(Boolean, default=True)  # Проверка ликвидности
    last_interest_change_date = Column(DateTime, nullable=True)  # Дата последнего изменения ставки
    penalty_fee = Column(Float, nullable=True)  # Штраф за просрочку платежа
    flexible_interest = Column(Boolean, default=False)  # Есть ли гибкая процентная ставка

    user = relationship("User", back_populates="financial_records")
