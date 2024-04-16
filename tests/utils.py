import aiofiles
from fastapi import UploadFile
from src.categories.schemas import CreateCategorySchema
from src.categories.models import Category
from src.categories.repository import CategoriesRepository
from src.products.schemas import CreateProductSchema
from src.products.repository import ProductsRepository
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


async def create_product(product: CreateProductSchema) -> Category:
    async with async_session_maker() as session:
        product_dict = product.model_dump()
        slug = slugify(product_dict["name"])
        product_dict["slug"] = slug
        image = product_dict["image"]
        image_location = f"media/images/{image.filename}"
        product_dict["image"] = image_location
        new_product = await ProductsRepository.add(db=session, values=product_dict)
        await _save_image(image_location, image)
        await session.commit()
        await session.refresh(new_product)
        return new_product


async def _save_image(image_location: str, image: UploadFile) -> None:
    async with aiofiles.open(image_location, "wb+") as file_object:
        content = await image.read()
        await file_object.write(content)
