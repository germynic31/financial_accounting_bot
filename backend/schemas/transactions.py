from typing import Optional

from pydantic import BaseModel, Field, field_validator

from tools.enums import TransactionEnum


class TransactionCreate(BaseModel):
    """Схема создания операции."""

    amount: float = Field(..., gt=0)
    type: TransactionEnum
    category_name: str = Field(..., min_length=1, max_length=50)
    description: Optional[str] = None

    @field_validator("amount")
    def round_amount(cls, value: float):
        return round(value, 2)