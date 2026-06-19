from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.category import Category
from app.repositories.base import BaseRepository
from app.schemas.category import CategoryCreate, CategoryUpdate


class CategoryRepository(BaseRepository[Category, CategoryCreate, CategoryUpdate]):
    def __init__(self, db: Session) -> None:
        super().__init__(Category, db)

    def get_by_name(self, name: str) -> Category | None:
        return self.db.query(Category).filter(func.lower(Category.name) == name.lower()).first()
