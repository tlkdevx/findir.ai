from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import FinancialRecord, User
from app.schemas import FinancialRecordCreate, UserCreate
from sqlalchemy.exc import IntegrityError

# ======= Операции с пользователями =======
async def create_user(db: AsyncSession, user: UserCreate):
    db_user = User(username=user.username, email=user.email, hashed_password=user.password)
    db.add(db_user)
    try:
        await db.commit()
        await db.refresh(db_user)
        return db_user
    except IntegrityError:
        return None

async def get_users(db: AsyncSession):
    result = await db.execute(select(User))
    return result.scalars().all()

async def get_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalars().first()

async def delete_user(db: AsyncSession, user_id: int):
    user = await get_user(db, user_id)
    if user:
        await db.delete(user)
        await db.commit()
        return True
    return False

# ======= Операции с финансовыми записями =======
async def create_financial_record(db: AsyncSession, user_id: int, record: FinancialRecordCreate):
    db_record = FinancialRecord(**record.dict(), user_id=user_id)
    db.add(db_record)
    await db.commit()
    await db.refresh(db_record)
    return db_record

async def get_financial_records(db: AsyncSession, user_id: int):
    result = await db.execute(select(FinancialRecord).where(FinancialRecord.user_id == user_id))
    records = result.scalars().all()

    # Преобразуем None в False (или другой безопасный дефолт)
    for record in records:
        record.is_open_ended = record.is_open_ended if record.is_open_ended is not None else False
        record.early_repayment_fee = record.early_repayment_fee if record.early_repayment_fee is not None else False
        record.overdraft_available = record.overdraft_available if record.overdraft_available is not None else False

    return records


async def delete_financial_record(db: AsyncSession, record_id: int):
    result = await db.execute(select(FinancialRecord).where(FinancialRecord.id == record_id))
    record = result.scalars().first()
    if record:
        await db.delete(record)
        await db.commit()
        return True
    return False
