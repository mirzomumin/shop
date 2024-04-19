from fastapi import APIRouter, Depends
from src.cart.schemas import GetCartSchema
from src.cart.service import CartService

router = APIRouter()


@router.post("/add/{product_id}")
async def cart_add(cart: GetCartSchema = Depends(CartService.add)) -> GetCartSchema:
    return cart


@router.post("/remove/{product_id}")
async def cart_remove(
    cart: GetCartSchema = Depends(CartService.remove),
) -> GetCartSchema:
    return cart


@router.get("/")
async def cart_detail(cart: GetCartSchema = Depends(CartService.get)) -> GetCartSchema:
    return cart
