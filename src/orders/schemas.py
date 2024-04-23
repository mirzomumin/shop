from decimal import Decimal
from pydantic import BaseModel, Field, EmailStr


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
    email: EmailStr
    address: str
    postal_code: str
    city: str
    paid: bool

    class ConfigDict:
        from_attributes = True

    @classmethod
    def from_db(cls, order):
        return cls(
            id=order.id,
            first_name=order.first_name,
            last_name=order.last_name,
            email=order.email,
            address=order.address,
            postal_code=order.postal_code,
            city=order.city,
            paid=order.paid,
        )


class OrderSchema(OrderSchemaList):
    items: list[OrderItem]
