from decimal import Decimal, ROUND_HALF_UP

from app.core.exceptions import NotFoundError
from app.repositories.budget_repository import BudgetRepository
from app.repositories.expense_repository import ExpenseRepository
from app.schemas.budget import BudgetCreate, BudgetStatus


class BudgetService:
    def __init__(self, budgets: BudgetRepository, expenses: ExpenseRepository) -> None:
        self.budgets = budgets
        self.expenses = expenses

    def create_or_update(self, user_id: int, data: BudgetCreate):
        return self.budgets.create_or_update(user_id, data)

    def status(self, user_id: int, year: int, month: int) -> BudgetStatus:
        budget = self.budgets.get_for_period(user_id, year, month)
        if not budget:
            raise NotFoundError("Budget not found for period")
        spent = self.expenses.monthly_total(user_id, year, month)
        remaining = budget.amount - spent
        utilization = Decimal("0.00")
        if budget.amount:
            utilization = ((spent / budget.amount) * 100).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        return BudgetStatus(
            month=month,
            year=year,
            budget_amount=budget.amount,
            spent_amount=spent,
            remaining_amount=remaining,
            utilization_percent=utilization,
            alert_threshold_percent=budget.alert_threshold_percent,
            is_alert=utilization >= budget.alert_threshold_percent,
        )
