from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .config import settings

engine = create_engine(settings.DATABASE_URL_DEV)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():  # TODO: сделать Session DI
    """Возвращает экземпляр сессии."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
