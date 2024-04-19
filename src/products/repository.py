from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from src.products.models import Product


class ProductsRepository:
    @classmethod
    async def add(cls, db: AsyncSession, values: dict) -> Product:
        stmt = insert(Product).values(**values).returning(Product)
        product = await db.execute(stmt)
        return product.scalar_one()

    @classmethod
    async def list(
        cls,
        db: AsyncSession,
        filter_by: dict = {},
    ) -> list[Product]:
        query = select(Product).filter_by(**filter_by)
        products = await db.execute(query)
        return products.scalars().all()

    @classmethod
    async def get(
        cls,
        id: int,
        db: AsyncSession,
    ) -> Product:
        query = select(Product).where(Product.id == id)
        product = await db.execute(query)
        return product.scalar()

    @classmethod
    async def update(
        cls,
        id: int,
        db: AsyncSession,
        values: dict = {},
    ) -> Product:
        stmt = (
            update(Product).where(Product.id == id).values(**values).returning(Product)
        )
        product = await db.execute(stmt)
        return product.scalar()

    @classmethod
    async def delete(
        cls,
        id: int,
        db: AsyncSession,
    ):
        stmt = delete(Product).where(Product.id == id).returning(Product.id)
        result = await db.execute(stmt)
        return result.scalar()

    @classmethod
    async def filter_by_ids(
        cls,
        ids: iter,
        db: AsyncSession,
    ):
        query = select(Product).filter(Product.id.in_(ids))
        products = await db.execute(query)
        return products.scalars().all()
