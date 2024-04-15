from src.categories.schemas import CreateCategorySchema
from src.categories.models import Category
from src.categories.repository import CategoriesRepository
from src.utils import slugify
from conftest import async_session_maker


async def create_category(category: CreateCategorySchema) -> Category:
    async with async_session_maker() as session:
        category_dict = category.model_dump()
        slug = slugify(category_dict["name"])
        category_dict["slug"] = slug
        new_category = await CategoriesRepository.add(db=session, values=category_dict)
        await session.commit()
        await session.refresh(new_category)
        return new_category
