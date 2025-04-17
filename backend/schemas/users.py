from typing import Optional

from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    """Схема создания пользователя."""

    telegram_id: int = Field(..., gt=0)
    username: Optional[str] = None
