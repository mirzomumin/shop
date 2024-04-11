from decimal import Decimal
from sqlalchemy import String, Text, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    name: Mapped[str] = mapped_column(String(200), index=True)
    slug: Mapped[str] = mapped_column(String(200), index=True)
    image: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(Text())
    price: Mapped[Decimal] = mapped_column(Numeric(precision=15, scale=2))
    is_available: Mapped[bool]
    # created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    # updated_at: Mapped[datetime.datetime] = mapped_column(
    #     server_default=FetchedValue(), server_onupdate=FetchedValue()
    # )

    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    category: Mapped["Category"] = relationship("Category", back_populates="products")  # noqa

    def __str__(self) -> str:
        return self.name
