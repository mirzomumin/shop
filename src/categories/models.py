from src.database import Base
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    name: Mapped[str] = mapped_column(String(200), index=True)
    slug: Mapped[str] = mapped_column(String(200), unique=True, index=True)

    # products: Mapped[list['Product']] = relationship('Product',
    #     back_populates='category', cascade='all, delete-orphan')

    def __str__(self) -> str:
        return self.name
