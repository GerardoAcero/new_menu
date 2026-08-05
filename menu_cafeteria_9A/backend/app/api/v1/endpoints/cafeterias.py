import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, require_roles
from app.core.database import get_db
from app.crud.cafeteria import cafeteria
from app.models.user import User, UserRole
from app.schemas.cafeteria import CafeteriaCreate, CafeteriaRead, CafeteriaUpdate

router = APIRouter()


@router.get("", response_model=list[CafeteriaRead])
async def list_cafeterias(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
) -> list:
    return await cafeteria.list(db, skip=skip, limit=limit, is_active=True)


@router.get("/{cafeteria_id}", response_model=CafeteriaRead)
async def get_cafeteria(
    cafeteria_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    obj = await cafeteria.get(db, cafeteria_id)
    if obj is None or not obj.is_active:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cafetería no encontrada")
    return obj


@router.post("", response_model=CafeteriaRead, status_code=status.HTTP_201_CREATED)
async def create_cafeteria(
    payload: CafeteriaCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.CAFETERIA_OWNER, UserRole.ADMIN)),
):
    return await cafeteria.create(db, payload, current_user.id)


@router.patch("/{cafeteria_id}", response_model=CafeteriaRead)
async def update_cafeteria(
    cafeteria_id: uuid.UUID,
    payload: CafeteriaUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    obj = await cafeteria.get(db, cafeteria_id)
    if obj is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cafetería no encontrada")
    if current_user.role != UserRole.ADMIN and obj.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No eres el dueño")
    return await cafeteria.update(db, obj, payload)
