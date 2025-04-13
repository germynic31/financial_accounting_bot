from sqlalchemy import func
from sqlalchemy.orm import Session

from crud.categories import get_or_create_category
from crud.limits import get_limit
from models import Transaction
from schemas.categories import CategoryCreate
from schemas.transactions import TransactionCreate
from tools.enums import TransactionEnum


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
