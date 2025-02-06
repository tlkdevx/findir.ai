from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text
from app.database import get_db
from app.schemas import UserCreate, UserResponse, FinancialRecordCreate, FinancialRecordResponse
from app.crud import (
    get_users, get_user, create_user, delete_user,
    create_financial_record, get_financial_records, delete_financial_record
)
from app.routes.optimizer import router as optimizer_router
from app.api.recommendations import router as recommendations_router  # ✅ ДОБАВЛЕН ИМПОРТ RECOMMENDATIONS
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Разрешаем CORS (чтобы frontend мог общаться с backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешает запросы со всех доменов (можно ограничить)
    allow_credentials=True,
    allow_methods=["*"],  # Разрешает все HTTP-методы (GET, POST, PUT, DELETE, OPTIONS)
    allow_headers=["*"],  # Разрешает все заголовки
)

# ✅ Добавляем маршруты
app.include_router(optimizer_router)
app.include_router(recommendations_router, prefix="/api")  # ✅ ДОБАВЛЕН ЭНДПОИНТ /recommendations

@app.get("/")
def read_root():
    return {"message": "Findir.ai API is running!"}

@app.get("/ping_db")
async def ping_db(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(text("SELECT 1"))
        return {"status": "Database connected", "result": result.scalar()}
    except Exception as e:
        return {"status": "Database connection failed", "error": str(e)}

# ✅ CRUD Пользователей
@app.post("/users", response_model=UserResponse)
async def create_new_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await create_user(db, user)
    if db_user is None:
        raise HTTPException(status_code=400, detail="User with this email already exists")
    return db_user

@app.get("/users", response_model=list[UserResponse])
async def read_users(db: AsyncSession = Depends(get_db)):
    return await get_users(db)

@app.get("/users/{user_id}", response_model=UserResponse)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.delete("/users/{user_id}")
async def remove_user(user_id: int, db: AsyncSession = Depends(get_db)):
    success = await delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted"}

# ✅ CRUD Финансовых данных
@app.post("/users/{user_id}/finance", response_model=FinancialRecordResponse)
async def add_financial_record(user_id: int, record: FinancialRecordCreate, db: AsyncSession = Depends(get_db)):
    return await create_financial_record(db, user_id, record)

@app.get("/users/{user_id}/finance", response_model=list[FinancialRecordResponse])
async def read_financial_records(user_id: int, db: AsyncSession = Depends(get_db)):
    return await get_financial_records(db, user_id)

@app.delete("/finance/{record_id}")
async def remove_financial_record(record_id: int, db: AsyncSession = Depends(get_db)):
    success = await delete_financial_record(db, record_id)
    if not success:
        raise HTTPException(status_code=404, detail="Record not found")
    return {"message": "Record deleted"}
