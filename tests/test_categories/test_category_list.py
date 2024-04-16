from httpx import AsyncClient

from tests.utils import create_category
from src.categories.schemas import CreateCategorySchema


async def test_list_category_empty(ac: AsyncClient):
    response = await ac.get("/categories/")

    assert response.status_code == 200
    assert len(response.json()) == 0


async def test_list_category_success(ac: AsyncClient):
    category_schema = CreateCategorySchema(name="Business")
    await create_category(category=category_schema)
    response = await ac.get("/categories/")

    category_data = response.json()[0]
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert category_data["name"] == "Business"
    assert category_data["slug"] == "business"
    assert "id" in category_data
