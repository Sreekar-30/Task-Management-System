from app.repositories.payment_method_repository import PaymentMethodRepository
from app.schemas.payment_method import PaymentMethodCreate


class PaymentMethodService:
    def __init__(self, methods: PaymentMethodRepository) -> None:
        self.methods = methods

    def seed_defaults(self) -> None:
        for name in ["Cash", "Credit Card", "Debit Card", "Bank Transfer", "UPI", "Wallet"]:
            self.methods.get_or_create(PaymentMethodCreate(name=name))
