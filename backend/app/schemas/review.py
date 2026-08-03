import uuid

from pydantic import BaseModel, ConfigDict, Field


class ReviewCreate(BaseModel):
    cafeteria_id: uuid.UUID
    order_id: uuid.UUID | None = None
    rating: int = Field(ge=1, le=5)
    comment: str | None = None


class ReviewRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    author_id: uuid.UUID
    cafeteria_id: uuid.UUID
    order_id: uuid.UUID | None
    rating: int
    comment: str | None
    created_at: object | None = None
