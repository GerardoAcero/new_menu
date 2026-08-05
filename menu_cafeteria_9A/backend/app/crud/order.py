from app.crud.base import CRUDBase
from app.models.order import Order, OrderItem
from app.models.review import Review
from app.schemas.order import OrderCreate, OrderStatusUpdate


class CRUDOrder(CRUDBase[Order, OrderCreate, OrderStatusUpdate]):
    async def create(self, db, obj_in: OrderCreate, client_id) -> Order:
        return await create_order_with_items(db, obj_in, client_id)


def create_order_with_items(db, obj_in: OrderCreate, client_id: int) -> Order:
    """Construye un pedido calculando totales. Se delega al service para crecer sin tocar el CRUD."""
    from app.services.orders import build_order

    return build_order(db, obj_in, client_id)


order = CRUDOrder(Order)


class CRUDReview(CRUDBase[Review, object, object]):
    pass


review = CRUDReview(Review)
