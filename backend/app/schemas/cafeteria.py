import uuid

from pydantic import BaseModel, ConfigDict, Field


class CafeteriaCreate(BaseModel):
    name: str = Field(min_length=2, max_length=150)
    description: str | None = None
    logo_url: str | None = None
    banner_url: str | None = None
    phone: str | None = None
    street: str = Field(min_length=1, max_length=255)
    city: str = Field(min_length=1, max_length=120)
    state: str | None = None
    postal_code: str | None = None
    country: str = "México"
    latitude: float | None = None
    longitude: float | None = None
    delivery_fee: float = 0
    min_order_amount: float = 0
    opens_at: str | None = None
    closes_at: str | None = None


class CafeteriaUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    logo_url: str | None = None
    banner_url: str | None = None
    phone: str | None = None
    street: str | None = None
    city: str | None = None
    state: str | None = None
    postal_code: str | None = None
    country: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    delivery_fee: float | None = None
    min_order_amount: float | None = None
    opens_at: str | None = None
    closes_at: str | None = None
    is_open: bool | None = None
    is_active: bool | None = None


class CafeteriaRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    owner_id: uuid.UUID
    name: str
    description: str | None
    logo_url: str | None
    banner_url: str | None
    phone: str | None
    street: str
    city: str
    state: str | None
    postal_code: str | None
    country: str
    latitude: float | None
    longitude: float | None
    delivery_fee: float
    min_order_amount: float
    is_open: bool
    is_active: bool
