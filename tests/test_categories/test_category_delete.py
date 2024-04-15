from httpx import AsyncClient

from tests.utils import create_category
from src.categories.schemas import CreateCategorySchema


async def test_delete_category_success(ac: AsyncClient):
    category_schema = CreateCategorySchema(name="IT")
    category = await create_category(category_schema)
    response = await ac.delete(f"/categories/{category.id}")

    assert response.status_code == 204


async def test_delete_category_fail(ac: AsyncClient):
    response = await ac.get("/categories/1")

    response_data = response.json()
    assert response.status_code == 404
    assert response_data["detail"] == "Object does not exist."
