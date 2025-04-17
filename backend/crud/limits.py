from sqlalchemy.orm import Session

from core.models import Limit
from schemas.limits import LimitCreate


def set_limit(db: Session, limit: LimitCreate):
    """Создает и возвращает лимит."""
    user_id = limit.user_id
    category_name = limit.category_name
    amount = limit.amount
    db.query(Limit).filter(
        Limit.user_id == user_id,
        Limit.category_name == category_name,
    ).delete()

    limit = Limit(
        user_id=user_id,
        category_name=category_name,
        amount=amount,
    )
    db.add(limit)
    db.commit()
    return limit


def get_limits(db: Session, user_id: int):
    """Возвращает лимиты."""
    return db.query(Limit).filter(Limit.user_id == user_id).all()


def get_limit(db: Session, user_id: int, category_name: str):
    """Возвращает лимит."""
    return db.query(Limit).filter(
        Limit.user_id == user_id,
        Limit.category_name == category_name,
    ).first()


def delete_limit(db: Session, user_id: int, category_name: str):
    """Удаляет лимит."""
    db.query(Limit).filter(
        Limit.user_id == user_id,
        Limit.category_name == category_name,
    ).delete()
    db.commit()
