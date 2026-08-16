import os
from logging.config import fileConfig
from sqlalchemy import create_engine
from alembic import context

# Подтягиваем модели
from app.models.domain import Base

config = context.config

if config.config_file_name:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

# Берём URL из .env (с фоллбэком)
db_url = os.getenv(
    "DATABASE_URL", 
    "postgresql://postgres:postgres_b2b_password@db:5432/enterprise_auth_db"
)
config.set_main_option("sqlalchemy.url", db_url)


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    # Создаем движок
    connectable = create_engine(db_url)

    # Открываем коннект без принудительного контекстного закрытия раньше времени
    connection = connectable.connect()
    
    try:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()
    finally:
        connection.close()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()