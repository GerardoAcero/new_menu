import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.core.database import get_db
from app.crud.order import order
from app.models.order import Order
from app.models.payment import Payment, PaymentMethod, PaymentStatus
from app.models.user import User
from app.schemas.payment import PaymentCreate, PaymentRead

router = APIRouter()


@router.post("/orders/{order_id}/payments", response_model=PaymentRead, status_code=status.HTTP_201_CREATED)
async def create_payment(
    order_id: uuid.UUID,
    payload: PaymentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    order_obj: Order | None = await order.get(db, order_id)
    if order_obj is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pedido no encontrado")
    if order_obj.client_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acceso denegado")

    payment = Payment(
        order_id=order_id,
        amount=float(order_obj.total),
        currency=order_obj.currency,
        method=payload.method,
        status=PaymentStatus.PENDING,
    )
    db.add(payment)
    await db.commit()
    await db.refresh(payment)
    return payment


@router.get("/orders/{order_id}/payments", response_model=PaymentRead | None)
async def get_payment_for_order(
    order_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    order_obj = await order.get(db, order_id)
    if order_obj is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pedido no encontrado")
    if order_obj.client_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acceso denegado")
    return order_obj.payment
