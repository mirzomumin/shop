from decimal import Decimal
from io import BytesIO
from httpx import AsyncClient
from fastapi import UploadFile

from src.categories.schemas import CreateCategorySchema
from src.products.schemas import CreateProductSchema
from tests.utils import create_category, create_product


async def test_add_product_to_cart_success(ac: AsyncClient):
    category_schema = CreateCategorySchema(name="IT")
    category = await create_category(category_schema)
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
    data = {"quantity": 2, "override": False}
    response = await ac.post(
        f"/cart/add/{product.id}",
        json=data,
    )

    response_data = response.json()
    product_data = response_data["cart"]["1"]["product"]
    cart_total_price_float = round(float(response_data["cart_total_price"]), 2)

    assert response.status_code == 200
    assert int(list(response_data["cart"].keys())[0]) == product.id
    assert product_data["id"] == product.id
    assert product_data["name"] == product.name
    assert product_data["slug"] == product.slug
    assert product_data["image"] == product.image
    assert product_data["description"] == product.description
    assert product_data["price"] == float(product.price)
    assert product_data["is_available"] == product.is_available
    assert product_data["category_id"] == product.category_id
    assert response_data["cart"]["1"]["quantity"] == data["quantity"]
    assert response_data["cart"]["1"]["price"] == float(product.price)
    assert (
        response_data["cart"]["1"]["total_price"]
        == float(product.price) * data["quantity"]
    )
    assert cart_total_price_float == float(product.price) * data["quantity"]
