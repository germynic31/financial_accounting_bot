from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base
from core.config import settings


engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """Создает базу данных."""
    Base.metadata.create_all(bind=engine)
