from decimal import Decimal
from pydantic import BaseModel, Field


class OrderItem(BaseModel):
    quantity: int
    price: Decimal
    product_id: int
    order_id: int

    class ConfigDict:
        from_attributes = True


class CreateOrderSchema(BaseModel):
    first_name: str = Field(..., max_length=60)
    last_name: str = Field(..., max_length=60)
    email: str = Field(..., max_length=250)
    address: str = Field(..., max_length=250)
    postal_code: str = Field(..., max_length=20)
    city: str = Field(..., max_length=100)

    class ConfigDict:
        from_attributes = True


class OrderSchemaList(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    address: str
    postal_code: str
    city: str

    class ConfigDict:
        from_attributes = True


class OrderSchema(OrderSchemaList):
    items: list[OrderItem]
