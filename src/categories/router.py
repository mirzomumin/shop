from fastapi import APIRouter, Depends, status

from src.categories.models import Category
from src.categories.schemas import CategorySchema
from src.categories.service import CategoriesService


router = APIRouter()


@router.post("/")
async def add_category(
    new_category: Category = Depends(CategoriesService.add),
) -> CategorySchema:
    return new_category


@router.get("/")
async def list_category(
    categories: list[Category] = Depends(CategoriesService.list),
) -> list[CategorySchema]:
    return categories


@router.get("/{id}")
async def get_category(
    category: Category = Depends(CategoriesService.get),
) -> CategorySchema:
    return category


@router.patch("/{id}")
async def update(
    updated_category: Category = Depends(CategoriesService.update),
) -> CategorySchema:
    return updated_category


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(result: None = Depends(CategoriesService.delete)) -> None:
    return result
