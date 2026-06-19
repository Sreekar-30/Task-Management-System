from datetime import date
from decimal import Decimal

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.repositories.category_repository import CategoryRepository
from app.repositories.expense_repository import ExpenseRepository
from app.repositories.payment_method_repository import PaymentMethodRepository
from app.schemas.common import Page
from app.schemas.expense import ExpenseCreate, ExpenseFilters, ExpenseRead, ExpenseUpdate
from app.services.expense_service import ExpenseService

router = APIRouter()


def get_service(db: Session = Depends(get_db)) -> ExpenseService:
    return ExpenseService(ExpenseRepository(db), CategoryRepository(db), PaymentMethodRepository(db))


@router.post("", response_model=ExpenseRead, status_code=status.HTTP_201_CREATED)
async def create_expense(data: ExpenseCreate, user: User = Depends(get_current_user), service: ExpenseService = Depends(get_service)):
    return service.create(data, user.id)


@router.get("", response_model=Page[ExpenseRead])
async def list_expenses(
    category_id: int | None = None,
    start_date: date | None = None,
    end_date: date | None = None,
    min_amount: Decimal | None = None,
    max_amount: Decimal | None = None,
    payment_method_id: int | None = None,
    search: str | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    sort_by: str = Query("expense_date", pattern="^(expense_date|amount|title|created_at)$"),
    sort_order: str = Query("desc", pattern="^(asc|desc)$"),
    user: User = Depends(get_current_user),
    service: ExpenseService = Depends(get_service),
):
    filters = ExpenseFilters(
        category_id=category_id,
        start_date=start_date,
        end_date=end_date,
        min_amount=min_amount,
        max_amount=max_amount,
        payment_method_id=payment_method_id,
        search=search,
        page=page,
        page_size=page_size,
        sort_by=sort_by,
        sort_order=sort_order,
    )
    items, total = service.list(user.id, filters)
    return Page[ExpenseRead](items=items, total=total, page=page, page_size=page_size)


@router.get("/{expense_id}", response_model=ExpenseRead)
async def get_expense(expense_id: int, user: User = Depends(get_current_user), service: ExpenseService = Depends(get_service)):
    return service.get(expense_id, user.id)


@router.put("/{expense_id}", response_model=ExpenseRead)
async def update_expense(
    expense_id: int,
    data: ExpenseUpdate,
    user: User = Depends(get_current_user),
    service: ExpenseService = Depends(get_service),
):
    return service.update(expense_id, user.id, data)


@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_expense(expense_id: int, user: User = Depends(get_current_user), service: ExpenseService = Depends(get_service)):
    service.delete(expense_id, user.id)
