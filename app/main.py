import sys
import os

# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import SessionLocal, engine
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Путь: app/main.py

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas import UserCreate, UserResponse, FinancialRecordCreate, FinancialRecordResponse
from app.crud import (
    get_users, get_user, create_user, delete_user,
    create_financial_record, get_financial_records, delete_financial_record,
    get_recommendations_from_db, create_test_financial_data  # Импортируем необходимые функции
)
from app.routes.optimizer import router as optimizer_router
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

# Добавляем маршруты
app.include_router(optimizer_router)

@app.get("/")
def read_root():
    return {"message": "Findir.ai API is running!"}

@app.get("/ping_db")
async def ping_db(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute("SELECT 1")
        return {"status": "Database connected", "result": result.scalar()}
    except Exception as e:
        return {"status": "Database connection failed", "error": str(e)}

# Создание второго пользователя и тестовых данных
@app.post("/users/create_test_user")
async def create_test_user(db: AsyncSession = Depends(get_db)):
    try:
        # Создаем второго пользователя
        user_data = UserCreate(username="user2", email="user2@example.com", password="password")
        new_user = await create_user(db, user_data)

        # Добавляем тестовые финансовые записи
        await create_test_financial_data(db, new_user.id)
        return {"message": "Test user created successfully", "user_id": new_user.id}
    except Exception as e:
        print(f"Error creating test user: {e}")  # Отладочный вывод
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

# CRUD Пользователей
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

# Финансовые записи для пользователя
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

# Маршрут для рекомендаций
@app.get("/api/recommendations")
async def get_recommendations(user_id: int, db: AsyncSession = Depends(get_db)):
    recommendations = await get_recommendations_from_db(db, user_id)
    if recommendations is None:
        raise HTTPException(status_code=404, detail="Recommendations not found")
    return recommendations

@app.get("/recommendations/{user_id}", response_model=schemas.Recommendation)
def get_recommendations(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    recommendations = crud.get_recommendations_from_db(db, user_id=user_id)
    logger.info(f"Recommendations for user {user_id}: {recommendations}")
    return recommendations
