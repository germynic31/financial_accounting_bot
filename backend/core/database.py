from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.config import settings
from models import Base

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """Создает базу данных."""
    Base.metadata.create_all(bind=engine)


def get_db():  # TODO: сделать Session DI
    """Возвращает экземпляр сессии."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
