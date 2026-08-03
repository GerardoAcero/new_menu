import uuid

from sqlalchemy import Boolean, ForeignKey, Integer, Numeric, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel


class MenuCategory(BaseModel):
    __tablename__ = "menu_categories"

    cafeteria_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("cafeterias.id", ondelete="CASCADE"), index=True, nullable=False
    )
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    cafeteria: Mapped["Cafeteria"] = relationship(back_populates="categories")  # noqa: F821
    products: Mapped[list["Product"]] = relationship(  # noqa: F821
        back_populates="category", cascade="all, delete-orphan"
    )

    __table_args__ = (
        UniqueConstraint("cafeteria_id", "name", name="uq_cafeteria_category_name"),
    )


class Product(BaseModel):
    __tablename__ = "products"

    cafeteria_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("cafeterias.id", ondelete="CASCADE"), index=True, nullable=False
    )
    category_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("menu_categories.id", ondelete="SET NULL"), nullable=True
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    base_price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="MXN", nullable=False)
    is_available: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_featured: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    preparation_time_min: Mapped[int | None] = mapped_column(Integer, nullable=True)

    cafeteria: Mapped["Cafeteria"] = relationship(back_populates="products")  # noqa: F821
    category: Mapped["MenuCategory | None"] = relationship(back_populates="products")  # noqa: F821
    options: Mapped[list["ProductOption"]] = relationship(  # noqa: F821
        back_populates="product", cascade="all, delete-orphan"
    )
    order_items: Mapped[list["OrderItem"]] = relationship(  # noqa: F821
        back_populates="product"
    )


class ProductOption(BaseModel):
    """Opciones y extras configurables de un producto (tamaño, añadidos, etc.)."""

    __tablename__ = "product_options"

    product_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("products.id", ondelete="CASCADE"), index=True, nullable=False
    )
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    price_modifier: Mapped[float] = mapped_column(Numeric(10, 2), default=0, nullable=False)
    is_available: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    product: Mapped["Product"] = relationship(back_populates="options")  # noqa: F821
