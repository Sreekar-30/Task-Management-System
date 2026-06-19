from sqlalchemy.orm import Session

from app.models.budget import Budget
from app.schemas.budget import BudgetCreate


class BudgetRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_for_period(self, user_id: int, year: int, month: int) -> Budget | None:
        return self.db.query(Budget).filter(Budget.user_id == user_id, Budget.year == year, Budget.month == month).first()

    def create_or_update(self, user_id: int, data: BudgetCreate) -> Budget:
        budget = self.get_for_period(user_id, data.year, data.month)
        if budget:
            budget.amount = data.amount
            budget.alert_threshold_percent = data.alert_threshold_percent
        else:
            budget = Budget(**data.model_dump(), user_id=user_id)
            self.db.add(budget)
        self.db.commit()
        self.db.refresh(budget)
        return budget
