from decimal import Decimal
from fastapi import UploadFile, File, Form
from pydantic import BaseModel, Field, field_validator
from src.products.constants import ACCEPTED_FILE_TYPES
from src.exceptions import InvalidMediaType


class CreateProductSchema(BaseModel):
    name: str = Field(..., max_length=200)
    image: UploadFile = File(..., media_type="image/jpeg")
    description: str | None
    price: Decimal = Field(..., ge=0)
    is_available: bool = True
    category_id: int = Field(..., gt=0)

    class ConfigDict:
        from_attributes = True

    @classmethod
    def as_form(
        cls,
        name: str = Form(..., max_length=200),
        description: str = Form(default=None),
        image: UploadFile = File(..., media_type="image/jpeg"),
        price: Decimal = Form(..., ge=0),
        is_available: bool = Form(default=True),
        category_id: int = Form(...),
    ):
        return cls(
            name=name,
            description=description,
            image=image,
            price=price,
            is_available=is_available,
            category_id=category_id,
        )

    @field_validator("image")
    def valid_image(cls, value: UploadFile):
        if value.content_type not in ACCEPTED_FILE_TYPES:
            raise InvalidMediaType
        return value


class UpdateProductSchema(CreateProductSchema):
    name: str | None
    image: UploadFile | None
    description: str | None
    price: Decimal | None
    is_available: bool | None
    category_id: int | None

    @classmethod
    def as_form(
        cls,
        name: str = Form(default=None, max_length=200),
        description: str = Form(default=None),
        image: UploadFile = File(default=None, media_type="image/jpeg"),
        price: Decimal = Form(default=None, ge=0),
        is_available: bool = Form(default=None),
        category_id: int = Form(default=None),
    ):
        return cls(
            name=name,
            description=description,
            image=image,
            price=price,
            is_available=is_available,
            category_id=category_id,
        )

    @field_validator("image")
    def valid_image(cls, value: UploadFile):
        if value is None:
            return value

        if value.content_type not in ACCEPTED_FILE_TYPES:
            raise InvalidMediaType
        return value


class ProductSchema(BaseModel):
    id: int
    name: str
    slug: str
    image: str
    description: str
    price: Decimal
    is_available: bool
    # created_at: datetime
    # updated_at: datetime
    category_id: int
