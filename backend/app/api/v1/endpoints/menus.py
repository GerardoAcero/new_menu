import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, require_roles
from app.core.database import get_db
from app.crud.cafeteria import cafeteria
from app.crud.menu import category, product
from app.models.user import User, UserRole
from app.schemas.menu import (
    CategoryCreate,
    CategoryRead,
    CategoryUpdate,
    ProductCreate,
    ProductRead,
    ProductUpdate,
)

router = APIRouter()


async def _own_cafeteria(db: AsyncSession, cafeteria_id: uuid.UUID, current_user: User) -> None:
    obj = await cafeteria.get(db, cafeteria_id)
    if obj is None or not obj.is_active:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cafetería no encontrada")
    if current_user.role != UserRole.ADMIN and obj.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No eres el dueño")


# ---- Categorías ----

@router.get("/cafeterias/{cafeteria_id}/categories", response_model=list[CategoryRead])
async def list_categories(
    cafeteria_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> list:
    return await category.list(db, cafeteria_id=cafeteria_id, is_active=True)


@router.post(
    "/cafeterias/{cafeteria_id}/categories",
    response_model=CategoryRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_category(
    cafeteria_id: uuid.UUID,
    payload: CategoryCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.CAFETERIA_OWNER, UserRole.ADMIN)),
):
    await _own_cafeteria(db, cafeteria_id, current_user)
    return await category.create(db, payload, cafeteria_id=cafeteria_id)


@router.patch("/categories/{category_id}", response_model=CategoryRead)
async def update_category(
    category_id: uuid.UUID,
    payload: CategoryUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.CAFETERIA_OWNER, UserRole.ADMIN)),
):
    obj = await category.get(db, category_id)
    if obj is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoría no encontrada")
    await _own_cafeteria(db, obj.cafeteria_id, current_user)
    return await category.update(db, obj, payload)


# ---- Productos ----

@router.get("/cafeterias/{cafeteria_id}/products", response_model=list[ProductRead])
async def list_products(
    cafeteria_id: uuid.UUID,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
) -> list:
    return await product.list(db, cafeteria_id=cafeteria_id, skip=skip, limit=limit)


@router.get("/products/{product_id}", response_model=ProductRead)
async def get_product(
    product_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    obj = await product.get(db, product_id)
    if obj is None or not obj.is_available:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
    return obj


@router.post(
    "/cafeterias/{cafeteria_id}/products",
    response_model=ProductRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_product(
    cafeteria_id: uuid.UUID,
    payload: ProductCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.CAFETERIA_OWNER, UserRole.ADMIN)),
):
    await _own_cafeteria(db, cafeteria_id, current_user)
    return await product.create(db, payload, cafeteria_id)


@router.patch("/products/{product_id}", response_model=ProductRead)
async def update_product(
    product_id: uuid.UUID,
    payload: ProductUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.CAFETERIA_OWNER, UserRole.ADMIN)),
):
    obj = await product.get(db, product_id)
    if obj is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
    await _own_cafeteria(db, obj.cafeteria_id, current_user)
    return await product.update(db, obj, payload)


@router.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.CAFETERIA_OWNER, UserRole.ADMIN)),
):
    obj = await product.get(db, product_id)
    if obj is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
    await _own_cafeteria(db, obj.cafeteria_id, current_user)
    await product.remove(db, obj)
