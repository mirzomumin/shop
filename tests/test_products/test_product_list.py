from decimal import Decimal
from io import BytesIO
from httpx import AsyncClient
from fastapi import UploadFile

from tests.utils import create_category, create_product
from src.categories.schemas import CreateCategorySchema
from src.products.schemas import CreateProductSchema


async def test_product_list_empty(ac: AsyncClient):
    response = await ac.get("/products/")

    assert response.status_code == 200
    assert len(response.json()) == 0


async def test_product_list_success(ac: AsyncClient):
    category_schema = CreateCategorySchema(name="Beverages")
    category = await create_category(category=category_schema)
    b_file = BytesIO(open("/home/mirzomumin/me.jpg", mode="rb").read())
    image_file = UploadFile(
        file=b_file, filename="image.jpg", headers={"content-type": "image/jpg"}
    )
    product_schema = CreateProductSchema(
        name="Green Tea",
        image=image_file,
        description=(
            "Lorem Ipsum is simply dummy text of "
            "the printing and typesetting industry. Lorem Ipsum "
            "has been the industry's standard dummy text ever since "
            "the 1500s, when an unknown printer took a galley of type"
            " and scrambled it to make a type specimen book."
        ),
        price=Decimal(109.99),
        is_available=True,
        category_id=category.id,
    )
    product = await create_product(product=product_schema)
    response = await ac.get("/products/")

    product_data = response.json()[0]
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert product_data["id"] == product.id
    assert product_data["name"] == product.name
    assert product_data["slug"] == product.slug
    assert product_data["description"] == product.description
    assert product_data["price"] == str(product.price)
    assert product_data["is_available"] == product.is_available
    assert product_data["category_id"] == product.category_id


async def test_product_list_with_params_success(ac: AsyncClient):
    category_schema = CreateCategorySchema(name="Beverages")
    category = await create_category(category=category_schema)
    b_file = BytesIO(open("/home/mirzomumin/me.jpg", mode="rb").read())
    image_file = UploadFile(
        file=b_file, filename="image.jpg", headers={"content-type": "image/jpg"}
    )
    product_schema = CreateProductSchema(
        name="Green Tea",
        image=image_file,
        description=(
            "Lorem Ipsum is simply dummy text of "
            "the printing and typesetting industry. Lorem Ipsum "
            "has been the industry's standard dummy text ever since "
            "the 1500s, when an unknown printer took a galley of type"
            " and scrambled it to make a type specimen book."
        ),
        price=Decimal(109.99),
        is_available=True,
        category_id=category.id,
    )
    product = await create_product(product=product_schema)

    category_schema = CreateCategorySchema(name="IT")
    category_2 = await create_category(category=category_schema)
    b_file = BytesIO(open("/home/mirzomumin/me.jpg", mode="rb").read())
    image_file = UploadFile(
        file=b_file, filename="image.jpg", headers={"content-type": "image/jpg"}
    )
    product_schema = CreateProductSchema(
        name="CRM system",
        image=image_file,
        description=(
            "CRM SYSTEM is simply dummy text of "
            "the printing and typesetting industry. Lorem Ipsum "
            "has been the industry's standard dummy text ever since "
            "the 1500s, when an unknown printer took a galley of type"
            " and scrambled it to make a type specimen book."
        ),
        price=Decimal(109.99),
        is_available=True,
        category_id=category_2.id,
    )
    product = await create_product(product=product_schema)
    response = await ac.get("/products/", params={"category_id": category_2.id})

    product_data = response.json()[0]
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert product_data["id"] == product.id
    assert product_data["name"] == product.name
    assert product_data["slug"] == product.slug
    assert product_data["description"] == product.description
    assert product_data["price"] == str(product.price)
    assert product_data["is_available"] == product.is_available
    assert product_data["category_id"] == product.category_id


async def test_product_list_with_params_empty(ac: AsyncClient):
    category_schema = CreateCategorySchema(name="Beverages")
    category = await create_category(category=category_schema)
    b_file = BytesIO(open("/home/mirzomumin/me.jpg", mode="rb").read())
    image_file = UploadFile(
        file=b_file, filename="image.jpg", headers={"content-type": "image/jpg"}
    )
    product_schema = CreateProductSchema(
        name="Green Tea",
        image=image_file,
        description=(
            "Lorem Ipsum is simply dummy text of "
            "the printing and typesetting industry. Lorem Ipsum "
            "has been the industry's standard dummy text ever since "
            "the 1500s, when an unknown printer took a galley of type"
            " and scrambled it to make a type specimen book."
        ),
        price=Decimal(109.99),
        is_available=True,
        category_id=category.id,
    )
    await create_product(product=product_schema)

    category_schema = CreateCategorySchema(name="IT")
    category_2 = await create_category(category=category_schema)
    b_file = BytesIO(open("/home/mirzomumin/me.jpg", mode="rb").read())
    image_file = UploadFile(
        file=b_file, filename="image.jpg", headers={"content-type": "image/jpg"}
    )
    product_schema = CreateProductSchema(
        name="CRM system",
        image=image_file,
        description=(
            "CRM SYSTEM is simply dummy text of "
            "the printing and typesetting industry. Lorem Ipsum "
            "has been the industry's standard dummy text ever since "
            "the 1500s, when an unknown printer took a galley of type"
            " and scrambled it to make a type specimen book."
        ),
        price=Decimal(109.99),
        is_available=True,
        category_id=category_2.id,
    )
    await create_product(product=product_schema)
    response = await ac.get("/products/", params={"category_id": 3000})

    assert response.status_code == 200
    assert len(response.json()) == 0
