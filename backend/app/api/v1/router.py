from fastapi import APIRouter

from app.api.v1.endpoints import (
    addresses,
    auth,
    cafeterias,
    menus,
    orders,
    payments,
    reviews,
    users,
)

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(addresses.router, prefix="/addresses", tags=["Addresses"])
api_router.include_router(cafeterias.router, prefix="/cafeterias", tags=["Cafeterias"])
api_router.include_router(menus.router, prefix="", tags=["Menus"])
api_router.include_router(orders.router, prefix="/orders", tags=["Orders"])
api_router.include_router(payments.router, prefix="", tags=["Payments"])
api_router.include_router(reviews.router, prefix="/reviews", tags=["Reviews"])
