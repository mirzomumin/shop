from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.exceptions import CartEmpty, ObjectNotFound
from src.cart.cart import Cart
from src.cart.service import CartService
from src.orders.schemas import CreateOrderSchema
from src.orders.repository import OrdersRepository, OrderItemsRepository
from src.database import get_db


class OrdersService:
    @classmethod
    async def create(
        cls,
        request: Request,
        create_order_schema: CreateOrderSchema,
        db: AsyncSession = Depends(get_db),
    ):
        cart_obj = Cart(request)
        if not cart_obj.cart:
            raise CartEmpty
        create_order_dict = create_order_schema.model_dump()
        try:
            order = await OrdersRepository.create(values=create_order_dict, db=db)
            card_obj = await CartService.get_updated_card_obj(cart_obj=cart_obj, db=db)
            cart = card_obj.cart

            item_list = []
            for _, item_obj in cart.items():
                item = {
                    "quantity": item_obj["quantity"],
                    "price": item_obj["price"],
                    "product_id": item_obj["product"]["id"],
                    "order_id": order.id,
                }
                item_list.append(item)
            await OrderItemsRepository.create(values=item_list, db=db)
        except Exception:
            await db.rollback()
        else:
            await db.commit()
            await db.refresh(order)
            cart_obj.clear()
            return order

    @classmethod
    async def list(cls, db: AsyncSession = Depends(get_db)):
        """Order List"""

        orders = await OrdersRepository.list(db=db)
        return orders

    @classmethod
    async def get(cls, id: int, db: AsyncSession = Depends(get_db)):
        """Order Detail"""
        order = await OrdersRepository.get(id=id, db=db)
        if order is None:
            raise ObjectNotFound
        return order
