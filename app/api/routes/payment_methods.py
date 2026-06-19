from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_roles
from app.core.enums import UserRole
from app.db.session import get_db
from app.models.user import User
from app.models.payment_method import PaymentMethod
from app.repositories.payment_method_repository import PaymentMethodRepository
from app.schemas.payment_method import PaymentMethodCreate, PaymentMethodRead

router = APIRouter()


@router.post("", response_model=PaymentMethodRead, status_code=status.HTTP_201_CREATED)
async def create_payment_method(
    data: PaymentMethodCreate,
    _: User = Depends(require_roles(UserRole.ADMIN)),
    db: Session = Depends(get_db),
):
    return PaymentMethodRepository(db).get_or_create(data)


@router.get("", response_model=list[PaymentMethodRead])
async def list_payment_methods(_: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(PaymentMethod).order_by(PaymentMethod.name.asc()).all()
