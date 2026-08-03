import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.core.database import get_db
from app.crud.order import review
from app.models.order import Order
from app.models.review import Review
from app.models.user import User
from app.schemas.review import ReviewCreate, ReviewRead

router = APIRouter()


@router.post("", response_model=ReviewRead, status_code=status.HTTP_201_CREATED)
async def create_review(
    payload: ReviewCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if payload.order_id is not None:
        order_obj: Order | None = await db.get(Order, payload.order_id)
        if order_obj is None or order_obj.client_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Solo puedes reseñar tus pedidos"
            )
    existing = await review.list(db, author_id=current_user.id, order_id=payload.order_id)
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Ya reseñaste este pedido")
    obj = Review(**payload.model_dump(), author_id=current_user.id)
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.get("/cafeterias/{cafeteria_id}/reviews", response_model=list[ReviewRead])
async def list_cafeteria_reviews(
    cafeteria_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> list:
    return await review.list(db, cafeteria_id=cafeteria_id)
