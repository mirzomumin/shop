from decimal import Decimal
from sqlalchemy import String, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    first_name: Mapped[str] = mapped_column(String(200))
    last_name: Mapped[str] = mapped_column(String(60))
    email: Mapped[str] = mapped_column(String(250))
    address: Mapped[str] = mapped_column(String(250))
    postal_code: Mapped[str] = mapped_column(String(20))
    city: Mapped[str] = mapped_column(String(100))
    # created_at
    # updated_at
    paid: Mapped[bool] = mapped_column(default=False)

    items: Mapped[list["OrderItem"]] = relationship(
        back_populates="order",
        cascade="all, delete-orphan",
    )

    def __str__(self) -> str:
        return f"Order: {self.id}"

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items)


class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    price: Mapped[Decimal] = mapped_column(Numeric(precision=15, scale=2))
    quantity: Mapped[int]

    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    order: Mapped["Order"] = relationship(back_populates="items")
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    product: Mapped["Product"] = relationship(  # noqa
        "Product", back_populates="order_items"
    )

    def __str__(self) -> str:
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity
