from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class BudgetCreate(BaseModel):
    month: int = Field(ge=1, le=12)
    year: int = Field(ge=2000, le=2100)
    amount: Decimal = Field(gt=0, max_digits=12, decimal_places=2)
    alert_threshold_percent: Decimal = Field(default=80, ge=1, le=100, max_digits=5, decimal_places=2)


class BudgetRead(BudgetCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    created_at: datetime


class BudgetStatus(BaseModel):
    month: int
    year: int
    budget_amount: Decimal
    spent_amount: Decimal
    remaining_amount: Decimal
    utilization_percent: Decimal
    alert_threshold_percent: Decimal
    is_alert: bool
