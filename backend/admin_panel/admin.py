from sqladmin import ModelView

from core.models import Category, Limit, Transaction, User


class UserAdmin(ModelView, model=User):
    """Класс пользователя в админке."""

    column_list = [
        User.id, User.telegram_id, User.username,
        User.role, User.password_hash, User.categories,
    ]


class CategoryAdmin(ModelView, model=Category):
    """Класс категории в админке."""

    column_list = [
        Category.id, Category.name, Category.user_id,
        Category.user, Category.transactions,
    ]


class TransactionAdmin(ModelView, model=Transaction):
    """Класс операции в админке."""

    column_list = [
        Transaction.id, Transaction.amount, Transaction.type,
        Transaction.description, Transaction.user_id,
        Transaction.category_id, Transaction.user, Transaction.category,
    ]


class LimitAdmin(ModelView, model=Limit):
    """Класс лимита в админке."""

    column_list = [
        Limit.id, Limit.user_id, Limit.category_name,
        Limit.amount, Limit.period, Limit.last_renewed,
        Limit.user,
    ]
