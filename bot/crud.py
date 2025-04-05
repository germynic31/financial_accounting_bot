from typing import Dict, List

from enums import TransactionEnum
from models import Category, Limit, Transaction, User
from schemas import CategoryCreate, LimitCreate, TransactionCreate, UserCreate
from sqlalchemy import func
from sqlalchemy.orm import Session


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


def get_or_create_category(db: Session, category: CategoryCreate) -> Category:
    """Создает или возвращает категорию."""
    db_category = db.query(Category).filter(
        Category.user_id == category.user_id,
        Category.name == category.name,
    ).first()
    if not db_category:
        db_category = Category(name=category.name, user_id=category.user_id)
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
    return db_category


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


def create_transaction(
        db: Session,
        transaction: TransactionCreate,
        user_id: int,
) -> dict[str, Transaction or str]:
    """Создает операцию."""
    category = get_or_create_category(
        db,
        CategoryCreate(name=transaction.category_name, user_id=user_id),
    )
    db_transaction = Transaction(
        amount=transaction.amount,
        type=transaction.type,
        category_id=category.id,
        user_id=user_id,
        description=transaction.description,
    )
    db.add(db_transaction)
    db.commit()

    if transaction.type == TransactionEnum.expense:
        limit = get_limit(db, user_id, transaction.category_name)
        if limit:
            spent = db.query(func.sum(Transaction.amount)).filter(
                Transaction.user_id == user_id,
                Transaction.category_id == category.id,
                Transaction.type == TransactionEnum.expense,
            ).scalar() or 0

            remaining = limit.amount - spent
            if remaining <= 0:
                return {"status": "error", "message": "Лимит превышен!"}
            if remaining <= limit.amount * 0.2:
                return {
                    "status": "warning",
                    "message": f"Осталось всего {remaining}"
                               f" ₽ из лимита {limit.amount} ₽",
                }

    return {"status": "success", "transaction": db_transaction}


def delete_limit(db: Session, user_id: int, category_name: str):
    """Удаляет лимит."""
    db.query(Limit).filter(
        Limit.user_id == user_id,
        Limit.category_name == category_name,
    ).delete()
    db.commit()
