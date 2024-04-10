from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from src.categories.models import Category


class CategoriesRepository:
    @classmethod
    async def add(cls, db: AsyncSession, values: dict) -> Category:
        stmt = insert(Category).values(**values).returning(Category)
        category = await db.execute(stmt)
        return category.scalar_one()

    @classmethod
    async def list(
        cls,
        db: AsyncSession,
        filter_by: dict = {},
    ) -> list[Category]:
        query = select(Category).filter_by(**filter_by)
        categories = await db.execute(query)
        return categories.scalars().all()

    @classmethod
    async def get(
        cls,
        id: int,
        db: AsyncSession,
    ) -> Category:
        query = select(Category).where(Category.id == id)
        category = await db.execute(query)
        return category.scalar()

    @classmethod
    async def update(
        cls,
        id: int,
        db: AsyncSession,
        values: dict = {},
    ) -> Category:
        stmt = (
            update(Category)
            .where(Category.id == id)
            .values(**values)
            .returning(Category)
        )
        category = await db.execute(stmt)
        return category.scalar()

    @classmethod
    async def delete(
        cls,
        id: int,
        db: AsyncSession,
    ):
        stmt = delete(Category).where(Category.id == id).returning(Category.id)
        result = await db.execute(stmt)
        return result.scalar()
