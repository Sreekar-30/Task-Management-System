from decimal import Decimal

from sqlalchemy import extract, func, or_
from sqlalchemy.orm import Session

from app.models.expense import Expense
from app.schemas.expense import ExpenseCreate, ExpenseFilters, ExpenseUpdate


class ExpenseRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_owned(self, expense_id: int, user_id: int) -> Expense | None:
        return self.db.query(Expense).filter(Expense.id == expense_id, Expense.user_id == user_id).first()

    def create(self, data: ExpenseCreate, user_id: int) -> Expense:
        expense = Expense(**data.model_dump(), user_id=user_id)
        self.db.add(expense)
        self.db.commit()
        self.db.refresh(expense)
        return expense

    def update(self, expense: Expense, data: ExpenseUpdate) -> Expense:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(expense, field, value)
        self.db.commit()
        self.db.refresh(expense)
        return expense

    def delete(self, expense: Expense) -> None:
        self.db.delete(expense)
        self.db.commit()

    def query_for_user(self, user_id: int, filters: ExpenseFilters):
        query = self.db.query(Expense).filter(Expense.user_id == user_id)
        if filters.category_id:
            query = query.filter(Expense.category_id == filters.category_id)
        if filters.start_date:
            query = query.filter(Expense.expense_date >= filters.start_date)
        if filters.end_date:
            query = query.filter(Expense.expense_date <= filters.end_date)
        if filters.min_amount is not None:
            query = query.filter(Expense.amount >= filters.min_amount)
        if filters.max_amount is not None:
            query = query.filter(Expense.amount <= filters.max_amount)
        if filters.payment_method_id:
            query = query.filter(Expense.payment_method_id == filters.payment_method_id)
        if filters.search:
            pattern = f"%{filters.search}%"
            query = query.filter(or_(Expense.title.ilike(pattern), Expense.description.ilike(pattern)))
        return query

    def list_filtered(self, user_id: int, filters: ExpenseFilters) -> tuple[list[Expense], int]:
        query = self.query_for_user(user_id, filters)
        total = query.count()
        sort_column = getattr(Expense, filters.sort_by)
        if filters.sort_order == "desc":
            sort_column = sort_column.desc()
        items = query.order_by(sort_column).offset((filters.page - 1) * filters.page_size).limit(filters.page_size).all()
        return items, total

    def monthly_total(self, user_id: int, year: int, month: int) -> Decimal:
        total = (
            self.db.query(func.coalesce(func.sum(Expense.amount), 0))
            .filter(Expense.user_id == user_id)
            .filter(extract("year", Expense.expense_date) == year)
            .filter(extract("month", Expense.expense_date) == month)
            .scalar()
        )
        return Decimal(total)
