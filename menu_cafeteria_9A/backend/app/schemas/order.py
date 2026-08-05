import uuid

from pydantic import BaseModel, ConfigDict, Field

from app.models.order import OrderStatus
from app.schemas.menu import ProductRead


class OrderItemCreate(BaseModel):
    product_id: uuid.UUID
    quantity: int = Field(gt=0, le=100)
    options: list[uuid.UUID] = []


class OrderCreate(BaseModel):
    cafeteria_id: uuid.UUID
    delivery_address: str = Field(min_length=5)
    notes: str | None = None
    items: list[OrderItemCreate] = Field(min_length=1)


class OrderItemRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    product_id: uuid.UUID
    product_name: str
    unit_price: float
    quantity: int
    line_total: float
    options_summary: str | None
    product: ProductRead | None = None


class OrderRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    client_id: uuid.UUID
    cafeteria_id: uuid.UUID
    status: OrderStatus
    subtotal: float
    delivery_fee: float
    service_fee: float
    total: float
    currency: str
    delivery_address: str
    notes: str | None
    created_at: object | None = None
    items: list[OrderItemRead] = []


class OrderStatusUpdate(BaseModel):
    status: OrderStatus
