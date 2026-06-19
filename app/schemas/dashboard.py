from decimal import Decimal

from pydantic import BaseModel


class TotalExpense(BaseModel):
    total: Decimal


class PeriodSummary(BaseModel):
    period: str
    total: Decimal


class CategorySpending(BaseModel):
    category_id: int
    category_name: str
    total: Decimal


class TrendPoint(BaseModel):
    date: str
    total: Decimal
