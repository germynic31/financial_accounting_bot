from typing import Optional

from enums import TransactionEnum
from pydantic import BaseModel, Field, field_validator


class TransactionCreate(BaseModel):
    """Схема создания операции."""

    amount: float = Field(..., gt=0)
    type: TransactionEnum
    category_name: str = Field(..., min_length=1, max_length=50)
    description: Optional[str] = None

    @field_validator("amount")
    def round_amount(cls, value: float):
        return round(value, 2)


class UserCreate(BaseModel):
    """Схема создания пользователя."""

    telegram_id: int = Field(..., gt=0)
    username: Optional[str] = None


class CategoryCreate(BaseModel):
    """Схема создания категории."""

    name: str = Field(..., min_length=1, max_length=50)
    user_id: int = Field(..., gt=0)


class LimitCreate(BaseModel):
    """Схема создания лимита."""

    user_id: int = Field(..., gt=0)
    category_name: str
    amount: float
