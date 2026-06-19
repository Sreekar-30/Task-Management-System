from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.repositories.dashboard_repository import DashboardRepository
from app.schemas.dashboard import CategorySpending, PeriodSummary, TotalExpense, TrendPoint
from app.services.dashboard_service import DashboardService

router = APIRouter()


def get_service(db: Session = Depends(get_db)) -> DashboardService:
    return DashboardService(DashboardRepository(db))


@router.get("/total", response_model=TotalExpense)
async def total_expenses(user: User = Depends(get_current_user), service: DashboardService = Depends(get_service)):
    return service.total(user.id)


@router.get("/monthly-summary", response_model=list[PeriodSummary])
async def monthly_summary(year: int | None = None, user: User = Depends(get_current_user), service: DashboardService = Depends(get_service)):
    return service.monthly_summary(user.id, year)


@router.get("/category-wise", response_model=list[CategorySpending])
async def category_wise(user: User = Depends(get_current_user), service: DashboardService = Depends(get_service)):
    return service.category_wise(user.id)


@router.get("/top-categories", response_model=list[CategorySpending])
async def top_categories(limit: int = Query(5, ge=1, le=20), user: User = Depends(get_current_user), service: DashboardService = Depends(get_service)):
    return service.top_categories(user.id, limit)


@router.get("/trends", response_model=list[TrendPoint])
async def trends(user: User = Depends(get_current_user), service: DashboardService = Depends(get_service)):
    return service.trends(user.id)


@router.get("/weekly-report", response_model=list[PeriodSummary])
async def weekly_report(year: int = date.today().year, user: User = Depends(get_current_user), service: DashboardService = Depends(get_service)):
    return service.weekly(user.id, year)


@router.get("/yearly-report", response_model=list[PeriodSummary])
async def yearly_report(user: User = Depends(get_current_user), service: DashboardService = Depends(get_service)):
    return service.yearly(user.id)
