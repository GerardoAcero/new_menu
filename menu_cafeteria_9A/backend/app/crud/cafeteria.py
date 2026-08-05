from app.crud.base import CRUDBase
from app.models.cafeteria import Cafeteria
from app.schemas.cafeteria import CafeteriaCreate, CafeteriaUpdate


class CRUDCafeteria(CRUDBase[Cafeteria, CafeteriaCreate, CafeteriaUpdate]):
    async def create(self, db, obj_in: CafeteriaCreate, owner_id) -> Cafeteria:
        obj = Cafeteria(**obj_in.model_dump(), owner_id=owner_id)
        db.add(obj)
        await db.commit()
        await db.refresh(obj)
        return obj


cafeteria = CRUDCafeteria(Cafeteria)
