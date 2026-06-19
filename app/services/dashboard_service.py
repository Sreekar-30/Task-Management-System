from decimal import Decimal

from app.repositories.dashboard_repository import DashboardRepository
from app.schemas.dashboard import CategorySpending, PeriodSummary, TotalExpense, TrendPoint


class DashboardService:
    def __init__(self, dashboard: DashboardRepository) -> None:
        self.dashboard = dashboard

    def total(self, user_id: int) -> TotalExpense:
        return TotalExpense(total=Decimal(self.dashboard.total_expenses(user_id)))

    def monthly_summary(self, user_id: int, year: int | None = None) -> list[PeriodSummary]:
        return [PeriodSummary(period=row.period, total=row.total) for row in self.dashboard.monthly_summary(user_id, year)]

    def category_wise(self, user_id: int) -> list[CategorySpending]:
        return [CategorySpending(category_id=row.id, category_name=row.name, total=row.total) for row in self.dashboard.category_wise(user_id)]

    def top_categories(self, user_id: int, limit: int = 5) -> list[CategorySpending]:
        return [CategorySpending(category_id=row.id, category_name=row.name, total=row.total) for row in self.dashboard.category_wise(user_id, limit)]

    def trends(self, user_id: int) -> list[TrendPoint]:
        return [TrendPoint(date=row.date, total=row.total) for row in self.dashboard.daily_trends(user_id)]

    def weekly(self, user_id: int, year: int) -> list[PeriodSummary]:
        return [PeriodSummary(period=row.period, total=row.total) for row in self.dashboard.weekly_report(user_id, year)]

    def yearly(self, user_id: int) -> list[PeriodSummary]:
        return [PeriodSummary(period=str(row.period), total=row.total) for row in self.dashboard.yearly_report(user_id)]
