from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.address import Address
from app.schemas.address import AddressCreate, AddressUpdate


class CRUDAddress(CRUDBase[Address, AddressCreate, AddressUpdate]):
    async def create(self, db: AsyncSession, obj_in: AddressCreate, user_id) -> Address:
        data = obj_in.model_dump()
        if data.get("is_default"):
            await db.execute(
                update(Address).where(Address.user_id == user_id).values(is_default=False)
            )
        obj = Address(**data, user_id=user_id)
        db.add(obj)
        await db.commit()
        await db.refresh(obj)
        return obj


address = CRUDAddress(Address)
