from httpx import AsyncClient

from tests.utils import create_category
from src.categories.schemas import CreateCategorySchema


async def test_get_category_success(ac: AsyncClient):
    category_schema = CreateCategorySchema(name="IT")
    category = await create_category(category_schema)
    response = await ac.get(f"/categories/{category.id}")

    category_data = response.json()
    assert response.status_code == 200
    assert category_data["id"] == category.id
    assert category_data["name"] == category.name
    assert category_data["slug"] == category.slug


async def test_get_category_fail(ac: AsyncClient):
    response = await ac.get("/categories/1")

    response_data = response.json()
    assert response.status_code == 404
    assert response_data["detail"] == "Object does not exist."
