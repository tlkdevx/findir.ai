from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# ====== Схемы пользователей ======
class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True  # Заменили orm_mode на from_attributes

# ====== Схемы финансовых данных ======
class FinancialRecordBase(BaseModel):
    type: str  # loan / deposit / credit_card
    bank_name: str
    amount: float
    interest_rate: float
    start_date: datetime
    end_date: Optional[datetime] = None  # Опционально для бессрочного депозита
    is_open_ended: bool = False  # Бессрочный депозит

    # Ограничения по суммам
    min_amount: Optional[float] = None
    max_amount: Optional[float] = None

    # Депозиты: разные модели начисления процентов
    interest_accrual_type: Optional[str] = None  # monthly_fixed_date / daily / floating
    future_date: Optional[datetime] = None

    # Кредиты: график платежей, штрафы
    payment_type: Optional[str] = None  # annuity / differentiated
    payment_day: Optional[int] = None  # День месяца для списания платежей
    early_repayment_fee: bool = False  # Штраф за досрочное погашение
    refinance_available: bool = False  # Доступно ли рефинансирование

    # Кредитные карты
    credit_limit: Optional[float] = None  # Лимит кредитной карты
    available_balance: Optional[float] = None  # Доступный баланс
    grace_period_end_date: Optional[datetime] = None  # Конец льготного периода
    purchase_interest_rate: Optional[float] = None  # Процентная ставка на покупки
    cash_withdrawal_rate: Optional[float] = None  # Ставка за снятие наличных
    refinance_rate: Optional[float] = None  # Ставка рефинансирования

    # Новые параметры
    monthly_fee: Optional[float] = None  # Ежемесячная комиссия
    cashback_percent: Optional[float] = None  # Процент кэшбэка
    overdraft_available: bool = False  # Возможность овердрафта
    overdraft_limit: Optional[float] = None  # Лимит овердрафта

class FinancialRecordCreate(FinancialRecordBase):
    pass

from typing import Optional

class FinancialRecordResponse(FinancialRecordBase):
    id: int
    user_id: int
    is_open_ended: Optional[bool] = None
    early_repayment_fee: Optional[bool] = None
    overdraft_available: Optional[bool] = None

    class Config:
        from_attributes = True  # Заменили orm_mode на from_attributes
