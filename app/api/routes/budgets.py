from fastapi import APIRouter, Depends, Path, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.repositories.budget_repository import BudgetRepository
from app.repositories.expense_repository import ExpenseRepository
from app.schemas.budget import BudgetCreate, BudgetRead, BudgetStatus
from app.services.budget_service import BudgetService

router = APIRouter()


def get_service(db: Session = Depends(get_db)) -> BudgetService:
    return BudgetService(BudgetRepository(db), ExpenseRepository(db))


@router.post("", response_model=BudgetRead, status_code=status.HTTP_201_CREATED)
async def create_budget(data: BudgetCreate, user: User = Depends(get_current_user), service: BudgetService = Depends(get_service)):
    return service.create_or_update(user.id, data)


@router.get("/status/{year}/{month}", response_model=BudgetStatus)
async def budget_status(
    year: int = Path(ge=2000, le=2100),
    month: int = Path(ge=1, le=12),
    user: User = Depends(get_current_user),
    service: BudgetService = Depends(get_service),
):
    return service.status(user.id, year, month)
