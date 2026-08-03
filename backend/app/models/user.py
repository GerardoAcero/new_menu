import enum
import uuid

from sqlalchemy import Boolean, Enum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel


class UserRole(str, enum.Enum):
    CLIENT = "client"
    CAFETERIA_OWNER = "cafeteria_owner"
    ADMIN = "admin"


class User(BaseModel):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(150), nullable=False)
    phone: Mapped[str | None] = mapped_column(String(30), nullable=True)
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole, name="user_role"), default=UserRole.CLIENT, nullable=False
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    addresses: Mapped[list["Address"]] = relationship(  # noqa: F821
        back_populates="user", cascade="all, delete-orphan"
    )
    owned_cafeterias: Mapped[list["Cafeteria"]] = relationship(  # noqa: F821
        back_populates="owner", foreign_keys="Cafeteria.owner_id"
    )
    orders: Mapped[list["Order"]] = relationship(  # noqa: F821
        back_populates="client", foreign_keys="Order.client_id"
    )
    reviews: Mapped[list["Review"]] = relationship(  # noqa: F821
        back_populates="author", cascade="all, delete-orphan"
    )
