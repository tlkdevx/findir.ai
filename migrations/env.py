from logging.config import fileConfig
from sqlalchemy import create_engine
from sqlalchemy import pool
from alembic import context

# Подключение конфигурации Alembic
config = context.config

# Настройка логирования
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Импорт моделей
from app.models import Base
target_metadata = Base.metadata

# Функция для миграций в оффлайн-режиме
def run_migrations_offline() -> None:
    """Запускает миграции в оффлайн-режиме."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

# Функция для миграций в онлайн-режиме
def run_migrations_online() -> None:
    """Запускает миграции в онлайн-режиме."""
    connectable = create_engine(config.get_main_option("sqlalchemy.url"), poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

# Определяем режим работы (онлайн/оффлайн)
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
