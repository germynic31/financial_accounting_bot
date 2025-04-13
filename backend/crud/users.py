from typing import Dict, List

from sqlalchemy import func
from sqlalchemy.orm import Session

from models import Category, Transaction, User
from schemas.users import UserCreate


def get_user(db: Session, telegram_id: int):
    """Возвращает пользователя по телеграм id."""
    return db.query(User).filter(User.telegram_id == telegram_id).first()


def create_user(db: Session, user: UserCreate):
    """Создает пользователя."""
    db_user = User(telegram_id=user.telegram_id, username=user.username)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_stats(db: Session, user_id: int) -> Dict:
    """Возвращает статистику пользователя."""
    # Доходы/расходы
    total_income = db.query(func.sum(Transaction.amount)).filter(
        Transaction.user_id == user_id,
        Transaction.type == "income",
    ).scalar() or 0

    total_expense = db.query(func.sum(Transaction.amount)).filter(
        Transaction.user_id == user_id,
        Transaction.type == "expense",
    ).scalar() or 0

    # Расходы по категориям
    expenses_by_category = db.query(
        Category.name,
        func.sum(Transaction.amount).label("total"),
    ).join(Transaction).filter(
        Transaction.user_id == user_id,
        Transaction.type == "expense",
    ).group_by(Category.name).all()

    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "balance": total_income - total_expense,
        "expenses_by_category": {
            cat[0]: cat[1] for cat in expenses_by_category
        },
    }


def get_user_transactions(
        db: Session,
        user_id: int,
        page: int = 1,
        per_page: int = 5,
) -> List[Transaction]:
    """Возвращает операции пользователя."""
    offset = (page - 1) * per_page
    return db.query(Transaction).filter(
        Transaction.user_id == user_id,
    ).order_by(
        Transaction.created_at.desc(),
    ).offset(offset).limit(per_page).all()
