from sqlalchemy import extract, func
from sqlalchemy.orm import Session

from app.models.category import Category
from app.models.expense import Expense


class DashboardRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def total_expenses(self, user_id: int):
        return self.db.query(func.coalesce(func.sum(Expense.amount), 0)).filter(Expense.user_id == user_id).scalar()

    def monthly_summary(self, user_id: int, year: int | None = None):
        period_expr = self._date_period("%Y-%m", "month").label("period")
        query = self.db.query(
            period_expr,
            func.coalesce(func.sum(Expense.amount), 0).label("total"),
        ).filter(Expense.user_id == user_id)
        if year:
            query = query.filter(extract("year", Expense.expense_date) == year)
        return query.group_by("period").order_by("period").all()

    def category_wise(self, user_id: int, limit: int | None = None):
        query = (
            self.db.query(Category.id, Category.name, func.coalesce(func.sum(Expense.amount), 0).label("total"))
            .join(Expense, Expense.category_id == Category.id)
            .filter(Expense.user_id == user_id)
            .group_by(Category.id, Category.name)
            .order_by(func.sum(Expense.amount).desc())
        )
        if limit:
            query = query.limit(limit)
        return query.all()

    def daily_trends(self, user_id: int):
        date_expr = self._date_period("%Y-%m-%d", "day").label("date")
        return (
            self.db.query(
                date_expr,
                func.coalesce(func.sum(Expense.amount), 0).label("total"),
            )
            .filter(Expense.user_id == user_id)
            .group_by("date")
            .order_by("date")
            .all()
        )

    def weekly_report(self, user_id: int, year: int):
        period_expr = self._week_period().label("period")
        return (
            self.db.query(
                period_expr,
                func.coalesce(func.sum(Expense.amount), 0).label("total"),
            )
            .filter(Expense.user_id == user_id, extract("year", Expense.expense_date) == year)
            .group_by("period")
            .order_by("period")
            .all()
        )

    def yearly_report(self, user_id: int):
        return (
            self.db.query(
                extract("year", Expense.expense_date).label("period"),
                func.coalesce(func.sum(Expense.amount), 0).label("total"),
            )
            .filter(Expense.user_id == user_id)
            .group_by("period")
            .order_by("period")
            .all()
        )

    def _date_period(self, mysql_format: str, sqlite_format: str):
        if self.db.bind and self.db.bind.dialect.name == "sqlite":
            formats = {"month": "%Y-%m", "day": "%Y-%m-%d"}
            return func.strftime(formats[sqlite_format], Expense.expense_date)
        return func.date_format(Expense.expense_date, mysql_format)

    def _week_period(self):
        if self.db.bind and self.db.bind.dialect.name == "sqlite":
            return func.strftime("%Y-W%W", Expense.expense_date)
        return func.concat(extract("year", Expense.expense_date), "-W", func.week(Expense.expense_date))
