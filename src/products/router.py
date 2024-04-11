from fastapi import APIRouter, Depends, status

from src.products.models import Product
from src.products.schemas import ProductSchema
from src.products.service import ProductsService


router = APIRouter()


@router.post("/")
async def add_product(
    new_product: Product = Depends(ProductsService.add),
) -> ProductSchema:
    return new_product


@router.get("/")
async def list_product(
    products: list[Product] = Depends(ProductsService.list),
) -> list[ProductSchema]:
    return products


@router.get("/{id}")
async def get_product(
    product: Product = Depends(ProductsService.get),
) -> ProductSchema:
    return product


@router.patch("/{id}")
async def update_product(
    updated_product: Product = Depends(ProductsService.update),
) -> ProductSchema:
    return updated_product


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(result: None = Depends(ProductsService.delete)) -> None:
    return result
