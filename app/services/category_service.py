from app.core.exceptions import ConflictError, NotFoundError
from app.repositories.category_repository import CategoryRepository
from app.schemas.category import CategoryCreate, CategoryUpdate


class CategoryService:
    def __init__(self, categories: CategoryRepository) -> None:
        self.categories = categories

    def create(self, data: CategoryCreate):
        if self.categories.get_by_name(data.name):
            raise ConflictError("Category already exists")
        return self.categories.create(data)

    def update(self, category_id: int, data: CategoryUpdate):
        category = self.categories.get(category_id)
        if not category:
            raise NotFoundError("Category not found")
        if data.name:
            existing = self.categories.get_by_name(data.name)
            if existing and existing.id != category_id:
                raise ConflictError("Category already exists")
        return self.categories.update(category, data)

    def delete(self, category_id: int) -> None:
        category = self.categories.get(category_id)
        if not category:
            raise NotFoundError("Category not found")
        self.categories.delete(category)
