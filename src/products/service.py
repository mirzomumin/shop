import aiofiles
from typing import Optional
from fastapi import Depends, UploadFile
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.products.schemas import CreateProductSchema, UpdateProductSchema
from src.products.repository import ProductsRepository
from src.products.models import Product
from src.database import get_db
from src.exceptions import ObjectNotFound, ObjectAlreadyExists
from src.utils import slugify


class ProductsService:
    @classmethod
    async def add(
        cls,
        product: CreateProductSchema = Depends(CreateProductSchema.as_form),
        db: AsyncSession = Depends(get_db),
    ) -> Product:
        product_dict = product.model_dump()
        slug = slugify(product_dict["name"])
        product_dict["slug"] = slug
        image = product_dict["image"]
        image_location = f"media/images/{image.filename}"
        product_dict["image"] = image_location
        try:
            new_product = await ProductsRepository.add(db=db, values=product_dict)
        except IntegrityError:
            raise ObjectAlreadyExists
        await cls._save_image(image_location, image)
        await db.commit()
        await db.refresh(new_product)
        return new_product

    @classmethod
    async def list(
        cls,
        category_id: Optional[int] = None,
        db: AsyncSession = Depends(get_db),
    ) -> list[Product]:
        params = {}
        if category_id:
            params = {"category_id": category_id}
        products = await ProductsRepository.list(db=db, filter_by=params)
        return products

    @classmethod
    async def get(
        cls,
        id: int,
        db: AsyncSession = Depends(get_db),
    ) -> Product:
        product = await ProductsRepository.get(id=id, db=db)
        if product is None:
            raise ObjectNotFound
        return product

    @classmethod
    async def update(
        cls,
        id: int,
        product: UpdateProductSchema = Depends(UpdateProductSchema.as_form),
        db: AsyncSession = Depends(get_db),
    ) -> Product:
        product_dict = product.model_dump(exclude_none=True, exclude_unset=True)
        product_name = product_dict.get("name")
        product_image = product_dict.get("image")
        if product_name:
            slug = slugify(product_name)
            product_dict["slug"] = slug
        if product_image:
            image_location = f"media/images/{product_image.filename}"
            product_dict["image"] = image_location
        try:
            updated_product = await ProductsRepository.update(
                id=id, values=product_dict, db=db
            )
        except IntegrityError:
            raise ObjectAlreadyExists
        if updated_product is None:
            raise ObjectNotFound
        if product_image:
            await cls._save_image(image_location=image_location, image=product_image)
        await db.commit()
        await db.refresh(updated_product)
        return updated_product

    @classmethod
    async def delete(
        cls,
        id: int,
        db: AsyncSession = Depends(get_db),
    ) -> None:
        result = await ProductsRepository.delete(id=id, db=db)
        if result is None:
            raise ObjectNotFound
        await db.commit()
        return

    @classmethod
    async def _save_image(cls, image_location: str, image: UploadFile) -> None:
        async with aiofiles.open(image_location, "wb+") as file_object:
            content = await image.read()
            await file_object.write(content)
