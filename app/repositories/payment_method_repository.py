from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.payment_method import PaymentMethod
from app.schemas.payment_method import PaymentMethodCreate


class PaymentMethodRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get(self, method_id: int) -> PaymentMethod | None:
        return self.db.get(PaymentMethod, method_id)

    def get_by_name(self, name: str) -> PaymentMethod | None:
        return self.db.query(PaymentMethod).filter(func.lower(PaymentMethod.name) == name.lower()).first()

    def get_or_create(self, data: PaymentMethodCreate) -> PaymentMethod:
        method = self.get_by_name(data.name)
        if method:
            return method
        method = PaymentMethod(**data.model_dump())
        self.db.add(method)
        self.db.commit()
        self.db.refresh(method)
        return method
