import uuid

from sqlalchemy import ForeignKey, Integer, Numeric, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel


class Review(BaseModel):
    __tablename__ = "reviews"

    author_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )
    cafeteria_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("cafeterias.id", ondelete="CASCADE"), index=True, nullable=False
    )
    order_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("orders.id", ondelete="SET NULL"), nullable=True
    )
    rating: Mapped[int] = mapped_column(Integer, nullable=False)
    comment: Mapped[str | None] = mapped_column(Text, nullable=True)

    author: Mapped["User"] = relationship(back_populates="reviews")  # noqa: F821
    cafeteria: Mapped["Cafeteria"] = relationship(back_populates="reviews")  # noqa: F821

    __table_args__ = (
        UniqueConstraint("author_id", "order_id", name="uq_author_order_review"),
    )
