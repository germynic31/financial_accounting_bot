from sqladmin import ModelView

from core.models import User


class UserAdmin(ModelView, model=User):
    """Класс пользователя в админке."""

    column_list = [
        User.id, User.telegram_id, User.username,
        User.role, User.password_hash, User.categories,
    ]
