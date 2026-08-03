from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.cafeteria import Cafeteria
from app.models.menu import Product, ProductOption
from app.models.order import Order, OrderItem
from app.schemas.order import OrderCreate


async def build_order(db: AsyncSession, obj_in: OrderCreate, client_id: int) -> Order:
    """Valida el carrito y construye el pedido con totales calculados."""
    cafeteria_obj = await db.get(Cafeteria, obj_in.cafeteria_id)
    if cafeteria_obj is None or not cafeteria_obj.is_active:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cafetería no encontrada")

    items: list[OrderItem] = []
    subtotal = Decimal("0")

    for item in obj_in.items:
        product_obj = await db.get(Product, item.product_id)
        if product_obj is None or product_obj.cafeteria_id != obj_in.cafeteria_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Producto {item.product_id} no pertenece a esta cafetería",
            )
        if not product_obj.is_available:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Producto '{product_obj.name}' no disponible",
            )

        unit_price = Decimal(str(product_obj.base_price))
        option_summaries: list[str] = []
        for option_id in item.options:
            option_obj = await db.get(ProductOption, option_id)
            if option_obj is None or option_obj.product_id != item.product_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Opción {option_id} inválida para el producto",
                )
            unit_price += Decimal(str(option_obj.price_modifier))
            option_summaries.append(option_obj.name)

        line_total = unit_price * item.quantity
        subtotal += line_total
        items.append(
            OrderItem(
                product_id=item.product_id,
                product_name=product_obj.name,
                unit_price=unit_price,
                quantity=item.quantity,
                line_total=line_total,
                options_summary=", ".join(option_summaries) or None,
            )
        )

    delivery_fee = Decimal(str(cafeteria_obj.delivery_fee))
    service_fee = Decimal("0")
    total = subtotal + delivery_fee + service_fee

    order_obj = Order(
        client_id=client_id,
        cafeteria_id=obj_in.cafeteria_id,
        subtotal=subtotal,
        delivery_fee=delivery_fee,
        service_fee=service_fee,
        total=total,
        currency="MXN",
        delivery_address=obj_in.delivery_address,
        notes=obj_in.notes,
        items=items,
    )
    db.add(order_obj)
    await db.commit()
    await db.refresh(order_obj)
    return order_obj


async def list_orders_for_user(db: AsyncSession, user_id: int) -> list[Order]:
    result = await db.execute(select(Order).where(Order.client_id == user_id).order_by(Order.created_at.desc()))
    return list(result.scalars().all())
