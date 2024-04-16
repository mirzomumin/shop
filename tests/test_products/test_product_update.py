from decimal import Decimal
from io import BytesIO
from httpx import AsyncClient
from fastapi import UploadFile

from tests.utils import create_category, create_product
from src.categories.schemas import CreateCategorySchema
from src.products.schemas import CreateProductSchema
from src.utils import slugify


async def test_product_update_success(ac: AsyncClient):
    # create product
    category_schema = CreateCategorySchema(name="Baverages")
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
    ############

    # update created product
    update_category_schema = CreateCategorySchema(name="Tea")
    update_category = await create_category(update_category_schema)
    update_image = open("/home/mirzomumin/passport.jpg", mode="rb").read()

    update_data = {
        "name": "Black Tea",
        "description": (
            "Lorem Ipsum is simply dummy text of "
            "the printing and typesetting industry. Lorem Ipsum "
            "has been the industry's standard dummy text ever since "
            "the 1500s, when an unknown printer took a galley of type"
            " and scrambled it to make a type specimen book."
        ),
        "price": "159.99",
        "is_available": True,
        "category_id": update_category.id,
    }

    response = await ac.patch(
        f"/products/{product.id}",
        data=update_data,
        files={"image": ("update_image.jpg", update_image)},
    )

    product_data = response.json()
    assert response.status_code == 200
    assert product_data["name"] == update_data["name"]
    assert product_data["slug"] == slugify(update_data["name"])
    assert product_data["description"] == update_data["description"]
    assert product_data["price"] == update_data["price"]
    assert product_data["is_available"] == update_data["is_available"]
    assert product_data["category_id"] == update_data["category_id"]
    assert product_data["image"] == "media/images/update_image.jpg"
    assert "id" in product_data


async def test_product_update_fail_404(ac: AsyncClient):
    # update created product
    update_category_schema = CreateCategorySchema(name="Tea")
    update_category = await create_category(update_category_schema)
    update_image = open("/home/mirzomumin/passport.jpg", mode="rb").read()

    update_data = {
        "name": "Black Tea",
        "description": (
            "Lorem Ipsum is simply dummy text of "
            "the printing and typesetting industry. Lorem Ipsum "
            "has been the industry's standard dummy text ever since "
            "the 1500s, when an unknown printer took a galley of type"
            " and scrambled it to make a type specimen book."
        ),
        "price": "159.99",
        "is_available": True,
        "category_id": update_category.id,
    }
    response = await ac.patch(
        "/products/1",
        data=update_data,
        files={"image": ("update_image.jpg", update_image)},
    )

    response_data = response.json()
    assert response.status_code == 404
    assert response_data["detail"] == "Object does not exist."


# async def test_product_create_fail_409(ac: AsyncClient):
#     # create category
#     category_schema = CreateCategorySchema(name="Beverages")
#     category = await create_category(category=category_schema)

#     # create first product
#     binary_file = open('/home/mirzomumin/me.jpg', mode='rb').read()
#     b_file = BytesIO(binary_file)
#     image_file = UploadFile(
#         file=b_file,
#         filename='image.jpg',
#         headers={"content-type": "image/jpg"})
#     data = {
#         "name": 'Green Tea',
#         "image": image_file,
#         "description": ("Lorem Ipsum is simply dummy text of "
#         "the printing and typesetting industry. Lorem Ipsum "
#         "has been the industry's standard dummy text ever since "
#         "the 1500s, when an unknown printer took a galley of type"
#         " and scrambled it to make a type specimen book."),
#         "price": Decimal(109.99),
#         "is_available": True,
#         "category_id": category.id,
#     }
#     product_schema = CreateProductSchema(**data)
#     product_1 = await create_product(product=product_schema)

#     # create second product
#     binary_file = open('/home/mirzomumin/passport.jpg', mode='rb').read()
#     b_file = BytesIO(binary_file)
#     image_file = UploadFile(
#         file=b_file,
#         filename='image.jpg',
#         headers={"content-type": "image/jpg"})
#     data = {
#         "name": 'Black Tea',
#         "image": image_file,
#         "description": ("Black Tea is simply dummy text of "
#         "the printing and typesetting industry. Lorem Ipsum "
#         "has been the industry's standard dummy text ever since "
#         "the 1500s, when an unknown printer took a galley of type"
#         " and scrambled it to make a type specimen book."),
#         "price": Decimal(119.99),
#         "is_available": True,
#         "category_id": category.id,
#     }
#     product_schema = CreateProductSchema(**data)
#     await create_product(product=product_schema)

#     # update product_1
#     data = {
#         'name': 'Black Tea',
#         'price': '105.99',
#     }

#     response = await ac.patch(
#         f"/products/{product_1.id}",
#         data=data,
#     )

#     assert response.status_code == 409
#     assert response.json()["detail"] == "Object already exists."
