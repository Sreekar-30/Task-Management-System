from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_roles
from app.core.enums import UserRole
from app.db.session import get_db
from app.models.user import User
from app.repositories.category_repository import CategoryRepository
from app.schemas.category import CategoryCreate, CategoryRead, CategoryUpdate
from app.services.category_service import CategoryService

router = APIRouter()


def get_service(db: Session = Depends(get_db)) -> CategoryService:
    return CategoryService(CategoryRepository(db))


@router.post("", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
async def create_category(
    data: CategoryCreate,
    _: User = Depends(require_roles(UserRole.ADMIN, UserRole.USER)),
    service: CategoryService = Depends(get_service),
):
    return service.create(data)


@router.get("", response_model=list[CategoryRead])
async def list_categories(
    _: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
):
    return CategoryRepository(db).list(skip, limit)


@router.put("/{category_id}", response_model=CategoryRead)
async def update_category(
    category_id: int,
    data: CategoryUpdate,
    _: User = Depends(require_roles(UserRole.ADMIN)),
    service: CategoryService = Depends(get_service),
):
    return service.update(category_id, data)


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: int,
    _: User = Depends(require_roles(UserRole.ADMIN)),
    service: CategoryService = Depends(get_service),
):
    service.delete(category_id)
