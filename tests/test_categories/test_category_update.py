from httpx import AsyncClient

from tests.utils import create_category
from src.categories.schemas import CreateCategorySchema


async def test_update_category_success(ac: AsyncClient):
    category_schema = CreateCategorySchema(name="IT")
    category = await create_category(category_schema)
    response = await ac.patch(f"/categories/{category.id}", json={"name": "Business"})

    category_data = response.json()
    assert response.status_code == 200
    assert category_data["id"] == category.id
    assert category_data["name"] == "Business"
    assert category_data["slug"] == "business"


async def test_update_category_fail_404(ac: AsyncClient):
    response = await ac.patch("/categories/1", json={"name": "Business"})

    response_data = response.json()
    assert response.status_code == 404
    assert response_data["detail"] == "Object does not exist."


async def test_update_category_fail_409(ac: AsyncClient):
    category_schema = CreateCategorySchema(name="Business")
    await create_category(category_schema)
    category_schema = CreateCategorySchema(name="IT")
    category = await create_category(category_schema)
    response = await ac.patch(f"/categories/{category.id}", json={"name": "Business"})

    response_data = response.json()
    assert response.status_code == 409
    assert response_data["detail"] == "Object already exists."
