from httpx import AsyncClient

from src.categories.schemas import CreateCategorySchema
from src.utils import slugify
from tests.utils import create_category


async def test_product_create_success(ac: AsyncClient):
    category_schema = CreateCategorySchema(name="Medicine")
    category = await create_category(category=category_schema)
    b_file = open("/home/mirzomumin/me.jpg", mode="rb").read()
    data = {
        "name": "Green Tea",
        "description": (
            "Lorem Ipsum is simply dummy text of "
            "the printing and typesetting industry. Lorem Ipsum "
            "has been the industry's standard dummy text ever since "
            "the 1500s, when an unknown printer took a galley of type"
            " and scrambled it to make a type specimen book."
        ),
        "price": "109.99",
        "is_available": True,
        "category_id": category.id,
    }
    response = await ac.post(
        "/products/",
        data=data,
        files={
            "image": ("image.jpg", b_file),
        },
    )

    product_data = response.json()
    assert response.status_code == 200
    assert product_data["name"] == data["name"]
    assert product_data["slug"] == slugify(data["name"])
    assert product_data["description"] == data["description"]
    assert product_data["price"] == data["price"]
    assert product_data["is_available"] == data["is_available"]
    assert product_data["category_id"] == data["category_id"]
    assert product_data["image"] == "media/images/image.jpg"
    assert "id" in product_data


# async def test_product_create_fail(ac: AsyncClient):
#     category_schema = CreateCategorySchema(name="Beverages")
#     category = await create_category(category=category_schema)
# binary_file = open('/home/mirzomumin/me.jpg', mode='rb').read()
# b_file = BytesIO(binary_file)
# image_file = UploadFile(
#     file=b_file,
#     filename='image.jpg',
#     headers={"content-type": "image/jpg"})
# data = {
#     "name": 'Green Tea',
#     "image": image_file,
#     "description": ("Lorem Ipsum is simply dummy text of "
#     "the printing and typesetting industry. Lorem Ipsum "
#     "has been the industry's standard dummy text ever since "
#     "the 1500s, when an unknown printer took a galley of type"
#     " and scrambled it to make a type specimen book."),
#     "price": Decimal(109.99),
#     "is_available": True,
#     "category_id": category.id,
# }
# product_schema = CreateProductSchema(**data)
# await create_product(product=product_schema)
#     data.pop('image')
#     data['price'] = str(data['price'])
#     response = await ac.post(
#         "/products/",
#         data=data,
#         files={'image': ('image.jpg', binary_file)}
#     )

#     assert response.status_code == 409
#     assert response.json()["detail"] == "Object already exists."
