from typing import Optional

from pydantic import BaseModel, Field, validator


class TransactionCreate(BaseModel):
    """Схема создания операции."""

    amount: float = Field(..., gt=0)
    type: str = Field(..., pattern="^(income|expense)$")
    category_name: str = Field(..., min_length=1, max_length=50)
    description: Optional[str] = None

    @validator("amount")
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
