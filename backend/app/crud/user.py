from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate


class CRUDUser(CRUDBase[User, UserCreate, object]):
    async def get_by_email(self, db: AsyncSession, email: str) -> User | None:
        result = await db.execute(select(User).where(User.email == email.lower()))
        return result.scalar_one_or_none()

    async def create(self, db: AsyncSession, obj_in: UserCreate) -> User:
        data = obj_in.model_dump()
        password = data.pop("password")
        data["email"] = data["email"].lower()
        user = User(**data, hashed_password=hash_password(password))
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user


user = CRUDUser(User)
