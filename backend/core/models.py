from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import declared_attr, relationship

from tools.enums import RoleEnum, TransactionEnum


@as_declarative()
class Base:
    """Базовая модель."""

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    @declared_attr
    def __tablename__(self) -> str:
        name = self.__name__.lower()
        return f'{name}ies' if name.endswith('y') else f'{name}s'

    def __repr__(self) -> str:
        return f'id: {self.id}. '


class User(Base):
    """Модель пользователя."""

    __tablename__ = 'users'
    telegram_id = Column(Integer, unique=True, nullable=False)
    username = Column(String)
    role = Column(Enum(RoleEnum), nullable=True, default=RoleEnum.user)
    password_hash = Column(String, nullable=True)

    categories = relationship('Category', back_populates='user')
    transactions = relationship('Transaction', back_populates='user')
    limits = relationship('Limit', back_populates='user')

    def __repr__(self) -> str:
        return f'{super().__repr__()}username: {self.username}'


class Category(Base):
    """Модель категории."""

    __tablename__ = 'categories'
    name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='categories')
    transactions = relationship('Transaction', back_populates='category')

    def __repr__(self) -> str:
        return f'{super().__repr__()}name: {self.name}'


class Transaction(Base):
    """Модель операции."""

    __tablename__ = 'transactions'
    amount = Column(Float, nullable=False)
    type = Column(Enum(TransactionEnum), nullable=False)
    description = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    category_id = Column(Integer, ForeignKey('categories.id'))
    user = relationship('User', back_populates='transactions')
    category = relationship('Category', back_populates='transactions')

    def __repr__(self) -> str:
        return f'{super().__repr__()}type: {self.type}. amount: {self.amount}'


class Limit(Base):
    """Модель лимита."""

    __tablename__ = 'limits'
    user_id = Column(Integer, ForeignKey('users.id'))
    category_name = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    period = Column(String, default='month')  # TODO: enum month/week/year
    last_renewed = Column(DateTime, default=datetime.now)
    user = relationship('User', back_populates='limits')

    def __repr__(self) -> str:
        return (
            f'{super().__repr__()}category_name: {self.category_name}.'
            f'amount: {self.amount}'
        )
