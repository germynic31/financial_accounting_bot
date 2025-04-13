from pydantic import BaseModel, Field


class CategoryCreate(BaseModel):
    """Схема создания категории."""

    name: str = Field(..., min_length=1, max_length=50)
    user_id: int = Field(..., gt=0)
