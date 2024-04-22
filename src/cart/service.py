import copy
from fastapi import Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.cart.schemas import AddCartProductSchema, CartProductSchema
from src.cart.cart import Cart
from src.exceptions import ObjectNotFound
from src.products.service import ProductsRepository
from src.database import get_db


class CartService:
    @classmethod
    async def add(
        cls,
        request: Request,
        product_id: int,
        cart_add_product_schema: AddCartProductSchema,
        db: AsyncSession = Depends(get_db),
    ) -> Cart:
        cart_obj = Cart(request)
        product = await ProductsRepository.get(id=product_id, db=db)
        if product is None:
            raise ObjectNotFound
        cart_add_product_dict = cart_add_product_schema.model_dump()
        await cart_obj.add(
            product=product,
            quantity=cart_add_product_dict["quantity"],
            override_quantity=cart_add_product_dict["override"],
        )
        cart_obj = await cls.get_updated_card_obj(cart_obj, db)
        return cart_obj

    @classmethod
    async def remove(
        cls,
        request: Request,
        product_id: int,
        db: AsyncSession = Depends(get_db),
    ) -> Cart:
        cart_obj = Cart(request)
        product = await ProductsRepository.get(id=product_id, db=db)
        if product is None:
            raise ObjectNotFound
        await cart_obj.remove(product=product)
        cart_obj = await cls.get_updated_card_obj(cart_obj, db)
        return cart_obj

    @classmethod
    async def get(
        cls,
        request: Request,
        db: AsyncSession = Depends(get_db),
    ) -> CartProductSchema:
        cart_obj = Cart(request)
        cart_obj = await cls.get_updated_card_obj(cart_obj, db)
        return cart_obj

    @staticmethod
    async def get_updated_card_obj(cart_obj: Cart, db: AsyncSession):
        cart_obj = copy.copy(cart_obj)  # copy of cart object
        cart = cart_obj.cart
        delattr(cart_obj, "session")
        product_ids = list(map(int, cart.keys()))
        products = await ProductsRepository.filter_by_ids(db=db, ids=product_ids)

        for product in products:
            cart[str(product.id)]["product"] = CartProductSchema.from_db(
                product
            ).model_dump()

        for item in cart.values():
            item["price"] = item["price"]
            item["total_price"] = item["price"] * item["quantity"]

        cart_obj.cart_total_price = cart_obj.get_total_price()
        return cart_obj
