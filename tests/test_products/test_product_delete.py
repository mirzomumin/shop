from decimal import Decimal
from io import BytesIO
from fastapi import UploadFile
from httpx import AsyncClient

from tests.utils import create_category, create_product
from src.categories.schemas import CreateCategorySchema
from src.products.schemas import CreateProductSchema


async def test_product_delete_success(ac: AsyncClient):
    category_schema = CreateCategorySchema(name="IT")
    category = await create_category(category_schema)

    binary_file = open("/home/mirzomumin/me.jpg", mode="rb").read()
    b_file = BytesIO(binary_file)
    image_file = UploadFile(
        file=b_file, filename="image.jpg", headers={"content-type": "image/jpg"}
    )
    data = {
        "name": "ERP-system",
        "image": image_file,
        "description": (
            "Lorem Ipsum is simply dummy text of "
            "the printing and typesetting industry. Lorem Ipsum "
            "has been the industry's standard dummy text ever since "
            "the 1500s, when an unknown printer took a galley of type"
            " and scrambled it to make a type specimen book."
        ),
        "price": Decimal(10500900.99),
        "is_available": True,
        "category_id": category.id,
    }
    product_schema = CreateProductSchema(**data)
    await create_product(product=product_schema)
    response = await ac.delete(f"/products/{category.id}")

    assert response.status_code == 204


async def test_product_delete_fail(ac: AsyncClient):
    response = await ac.get("/products/1")

    response_data = response.json()
    assert response.status_code == 404
    assert response_data["detail"] == "Object does not exist."
