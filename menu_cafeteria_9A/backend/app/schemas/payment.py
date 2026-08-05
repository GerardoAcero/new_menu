import uuid

from pydantic import BaseModel, ConfigDict

from app.models.payment import PaymentMethod, PaymentStatus


class PaymentCreate(BaseModel):
    method: PaymentMethod


class PaymentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    order_id: uuid.UUID
    amount: float
    currency: str
    method: PaymentMethod
    status: PaymentStatus
    provider: str | None
    provider_reference: str | None
    paid_at: object | None = None
