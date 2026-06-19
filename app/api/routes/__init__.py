from fastapi import APIRouter

from app.api.routes import auth, budgets, categories, dashboard, expenses, health, payment_methods

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(categories.router, prefix="/categories", tags=["categories"])
api_router.include_router(payment_methods.router, prefix="/payment-methods", tags=["payment methods"])
api_router.include_router(expenses.router, prefix="/expenses", tags=["expenses"])
api_router.include_router(budgets.router, prefix="/budgets", tags=["budgets"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
