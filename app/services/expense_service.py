from app.core.exceptions import NotFoundError
from app.repositories.category_repository import CategoryRepository
from app.repositories.expense_repository import ExpenseRepository
from app.repositories.payment_method_repository import PaymentMethodRepository
from app.schemas.expense import ExpenseCreate, ExpenseFilters, ExpenseUpdate


class ExpenseService:
    def __init__(
        self,
        expenses: ExpenseRepository,
        categories: CategoryRepository,
        payment_methods: PaymentMethodRepository,
    ) -> None:
        self.expenses = expenses
        self.categories = categories
        self.payment_methods = payment_methods

    def create(self, data: ExpenseCreate, user_id: int):
        self._validate_refs(data.category_id, data.payment_method_id)
        return self.expenses.create(data, user_id)

    def update(self, expense_id: int, user_id: int, data: ExpenseUpdate):
        expense = self.get(expense_id, user_id)
        if data.category_id or data.payment_method_id:
            self._validate_refs(data.category_id or expense.category_id, data.payment_method_id or expense.payment_method_id)
        return self.expenses.update(expense, data)

    def get(self, expense_id: int, user_id: int):
        expense = self.expenses.get_owned(expense_id, user_id)
        if not expense:
            raise NotFoundError("Expense not found")
        return expense

    def delete(self, expense_id: int, user_id: int) -> None:
        self.expenses.delete(self.get(expense_id, user_id))

    def list(self, user_id: int, filters: ExpenseFilters):
        return self.expenses.list_filtered(user_id, filters)

    def _validate_refs(self, category_id: int, payment_method_id: int) -> None:
        if not self.categories.get(category_id):
            raise NotFoundError("Category not found")
        if not self.payment_methods.get(payment_method_id):
            raise NotFoundError("Payment method not found")
