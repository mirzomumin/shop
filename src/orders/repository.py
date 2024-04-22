from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select
from sqlalchemy.orm import joinedload

from src.orders.models import Order, OrderItem


class OrdersRepository:
    @classmethod
    async def create(
        cls,
        values: dict,
        db: AsyncSession,
    ) -> Order:
        stmt = (
            insert(Order)
            .values(**values)
            .options(joinedload(Order.items))
            .returning(Order)
        )
        order = await db.execute(stmt)
        return order.unique().scalar_one()

    @classmethod
    async def list(cls, db: AsyncSession, filter_by: dict = {}):
        query = select(Order).filter_by(**filter_by)
        orders = await db.execute(query)
        return orders.scalars().all()

    @classmethod
    async def get(cls, id: int, db: AsyncSession):
        query = select(Order).options(joinedload(Order.items)).where(Order.id == id)
        orders = await db.execute(query)
        return orders.scalar()


class OrderItemsRepository:
    @classmethod
    async def create(
        cls,
        values: list[dict],
        db: AsyncSession,
    ) -> list[OrderItem]:
        stmt = insert(OrderItem).returning(OrderItem)
        items = await db.execute(stmt, values)
        return items.scalars().all()
