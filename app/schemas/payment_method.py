from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class PaymentMethodBase(BaseModel):
    name: str = Field(min_length=2, max_length=80)
    description: str | None = Field(default=None, max_length=255)


class PaymentMethodCreate(PaymentMethodBase):
    pass


class PaymentMethodRead(PaymentMethodBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
