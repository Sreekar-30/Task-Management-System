from sqlalchemy import Index, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin


class PaymentMethod(Base, TimestampMixin):
    __tablename__ = "payment_methods"
    __table_args__ = (Index("ix_payment_methods_name", "name"),)

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(String(255))

    expenses = relationship("Expense", back_populates="payment_method")
