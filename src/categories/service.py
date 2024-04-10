from fastapi import Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.categories.schemas import CreateCategorySchema, UpdateCategorySchema
from src.categories.repository import CategoriesRepository
from src.categories.models import Category
from src.database import get_db
from src.exceptions import ObjectNotFound, ObjectAlreadyExists
from src.utils import slugify


class CategoriesService:
    @classmethod
    async def add(
        cls,
        category: CreateCategorySchema,
        db: AsyncSession = Depends(get_db),
    ) -> Category:
        category_dict = category.model_dump()
        slug = slugify(category_dict["name"])
        category_dict["slug"] = slug
        try:
            new_category = await CategoriesRepository.add(db=db, values=category_dict)
        except IntegrityError:
            raise ObjectAlreadyExists
        await db.commit()
        await db.refresh(new_category)
        return new_category

    @classmethod
    async def list(
        cls,
        db: AsyncSession = Depends(get_db),
    ) -> list[Category]:
        categories = await CategoriesRepository.list(db=db)
        return categories

    @classmethod
    async def get(
        cls,
        id: int,
        db: AsyncSession = Depends(get_db),
    ) -> Category:
        category = await CategoriesRepository.get(id=id, db=db)
        if category is None:
            raise ObjectNotFound
        return category

    @classmethod
    async def update(
        cls,
        id: int,
        category: UpdateCategorySchema,
        db: AsyncSession = Depends(get_db),
    ) -> Category:
        category_dict = category.model_dump()
        slug = slugify(category_dict["name"])
        category_dict["slug"] = slug
        try:
            updated_category = await CategoriesRepository.update(
                id=id, values=category_dict, db=db
            )
        except IntegrityError:
            raise ObjectAlreadyExists
        if updated_category is None:
            raise ObjectNotFound
        await db.commit()
        await db.refresh(updated_category)
        return updated_category

    @classmethod
    async def delete(
        cls,
        id: int,
        db: AsyncSession = Depends(get_db),
    ) -> None:
        result = await CategoriesRepository.delete(id=id, db=db)
        if result is None:
            raise ObjectNotFound
        await db.commit()
        return
