from fastapi import APIRouter, Depends
from src.orders.schemas import OrderSchema, OrderSchemaList
from src.orders.models import Order
from src.orders.service import OrdersService

router = APIRouter()


@router.post("/")
async def order_create(order: Order = Depends(OrdersService.create)) -> OrderSchema:
    """Order create for customers"""
    return order


@router.get("/")
async def order_list(
    orders: list[Order] = Depends(OrdersService.list),
) -> list[OrderSchemaList]:
    """Order List"""
    return orders


@router.get("/{id}")
async def order_detail(orders: Order = Depends(OrdersService.get)) -> OrderSchema:
    """Order Detail"""
    return orders
