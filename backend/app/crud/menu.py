from app.crud.base import CRUDBase
from app.models.menu import MenuCategory, Product, ProductOption
from app.schemas.menu import CategoryCreate, CategoryUpdate, ProductCreate, ProductUpdate


class CRUDCategory(CRUDBase[MenuCategory, CategoryCreate, CategoryUpdate]):
    pass


class CRUDProduct(CRUDBase[Product, ProductCreate, ProductUpdate]):
    async def create(self, db, obj_in: ProductCreate, cafeteria_id) -> Product:
        data = obj_in.model_dump(exclude={"options"})
        options_data = obj_in.options
        product = Product(**data, cafeteria_id=cafeteria_id)
        for opt in options_data:
            product.options.append(ProductOption(**opt.model_dump()))
        db.add(product)
        await db.commit()
        await db.refresh(product)
        return product


category = CRUDCategory(MenuCategory)
product = CRUDProduct(Product)
