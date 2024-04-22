from decimal import Decimal
from fastapi import Path
from pydantic import BaseModel

from src.products.schemas import CartProductSchema


class AddCartProductSchema(BaseModel):
    quantity: int = Path(..., gt=0, le=21)
    override: bool = False


class CartSchema(BaseModel):
    product: CartProductSchema
    quantity: int
    price: float
    total_price: float

    class ConfigDict:
        orm_mode = True


class GetCartSchema(BaseModel):
    cart: dict[str, CartSchema]
    cart_total_price: Decimal

    # class ConfigDict:
    #     from_attributes = True
