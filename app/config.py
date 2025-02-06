from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://postgres:tlkdevpass@localhost:5432/findir"

    class Config:
        env_file = ".env"

settings = Settings()
