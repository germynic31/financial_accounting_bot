from enum import Enum


class TransactionEnum(str, Enum):
    """Типы транзакций."""

    income = 'income'
    expense = 'expense'


class PeriodEnum(str, Enum):
    """Типы периода."""

    week = 'week'
    month = 'month'
    year = 'year'


class RoleEnum(str, Enum):
    """Роли пользователей в системе."""

    user = 'user'
    admin = 'admin'
