import uuid

from pydantic import BaseModel, ConfigDict, Field


class AddressCreate(BaseModel):
    label: str = Field(min_length=1, max_length=80)
    street: str = Field(min_length=1, max_length=255)
    number: str | None = None
    city: str = Field(min_length=1, max_length=120)
    state: str | None = None
    postal_code: str | None = None
    country: str = "México"
    reference: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    is_default: bool = False


class AddressUpdate(BaseModel):
    label: str | None = None
    street: str | None = None
    number: str | None = None
    city: str | None = None
    state: str | None = None
    postal_code: str | None = None
    country: str | None = None
    reference: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    is_default: bool | None = None


class AddressRead(AddressCreate):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    user_id: uuid.UUID
