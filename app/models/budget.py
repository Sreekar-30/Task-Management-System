from decimal import Decimal

from sqlalchemy import CheckConstraint, ForeignKey, Index, Numeric, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin


class Budget(Base, TimestampMixin):
    __tablename__ = "budgets"
    __table_args__ = (
        CheckConstraint("amount > 0", name="ck_budgets_amount_positive"),
        CheckConstraint("month >= 1 AND month <= 12", name="ck_budgets_month"),
        UniqueConstraint("user_id", "month", "year", name="uq_budgets_user_month_year"),
        Index("ix_budgets_user_period", "user_id", "year", "month"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    month: Mapped[int] = mapped_column(nullable=False)
    year: Mapped[int] = mapped_column(nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    alert_threshold_percent: Mapped[Decimal] = mapped_column(Numeric(5, 2), default=80, nullable=False)

    user = relationship("User", back_populates="budgets")
