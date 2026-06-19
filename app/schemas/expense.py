from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class ExpenseBase(BaseModel):
    title: str = Field(min_length=2, max_length=140)
    amount: Decimal = Field(gt=0, max_digits=12, decimal_places=2)
    expense_date: date
    category_id: int
    payment_method_id: int
    description: str | None = None


class ExpenseCreate(ExpenseBase):
    pass


class ExpenseUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=2, max_length=140)
    amount: Decimal | None = Field(default=None, gt=0, max_digits=12, decimal_places=2)
    expense_date: date | None = None
    category_id: int | None = None
    payment_method_id: int | None = None
    description: str | None = None


class ExpenseRead(ExpenseBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime


class ExpenseFilters(BaseModel):
    category_id: int | None = None
    start_date: date | None = None
    end_date: date | None = None
    min_amount: Decimal | None = Field(default=None, ge=0)
    max_amount: Decimal | None = Field(default=None, ge=0)
    payment_method_id: int | None = None
    search: str | None = None
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)
    sort_by: str = Field(default="expense_date", pattern="^(expense_date|amount|title|created_at)$")
    sort_order: str = Field(default="desc", pattern="^(asc|desc)$")
