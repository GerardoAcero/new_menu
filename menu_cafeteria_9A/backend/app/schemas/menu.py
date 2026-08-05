import uuid

from pydantic import BaseModel, ConfigDict, Field


class ProductOptionSchema(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    price_modifier: float = 0
    is_available: bool = True


class ProductOptionRead(ProductOptionSchema):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID


class ProductCreate(BaseModel):
    category_id: uuid.UUID | None = None
    name: str = Field(min_length=1, max_length=200)
    description: str | None = None
    image_url: str | None = None
    base_price: float = Field(gt=0)
    currency: str = "MXN"
    is_available: bool = True
    is_featured: bool = False
    preparation_time_min: int | None = None
    options: list[ProductOptionSchema] = []


class ProductUpdate(BaseModel):
    category_id: uuid.UUID | None = None
    name: str | None = None
    description: str | None = None
    image_url: str | None = None
    base_price: float | None = None
    currency: str | None = None
    is_available: bool | None = None
    is_featured: bool | None = None
    preparation_time_min: int | None = None


class ProductRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    cafeteria_id: uuid.UUID
    category_id: uuid.UUID | None
    name: str
    description: str | None
    image_url: str | None
    base_price: float
    currency: str
    is_available: bool
    is_featured: bool
    preparation_time_min: int | None
    options: list[ProductOptionRead] = []


class CategoryCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    description: str | None = None
    sort_order: int = 0


class CategoryUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    sort_order: int | None = None
    is_active: bool | None = None


class CategoryRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    cafeteria_id: uuid.UUID
    name: str
    description: str | None
    sort_order: int
    is_active: bool
