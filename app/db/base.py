import os
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

# Берем из окружения (.env), а если нет — фоллбэк на докеровский хост `db`
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://postgres:postgres_b2b_password@db:5432/enterprise_auth_db"
)

# Движок управления пулом соединений
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Проверяет живое ли соединение перед запросом
    pool_size=10,        # Размер пула соединений
    max_overflow=20      # Максимальное количество временных переполнений пула
)

# Фабрика сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency для FastAPI
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()