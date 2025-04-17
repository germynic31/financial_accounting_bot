from sqlalchemy.orm import Session

from core.models import Category
from schemas.categories import CategoryCreate


def get_or_create_category(db: Session, category: CategoryCreate) -> Category:
    """Создает или возвращает категорию."""
    db_category = db.query(Category).filter(
        Category.user_id == category.user_id,
        Category.name == category.name,
    ).first()
    if not db_category:
        db_category = Category(name=category.name, user_id=category.user_id)
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
    return db_category
