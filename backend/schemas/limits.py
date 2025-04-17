from pydantic import BaseModel, Field


class LimitCreate(BaseModel):
    """Схема создания лимита."""

    user_id: int = Field(..., gt=0)
    category_name: str
    amount: float
