from httpx import AsyncClient

from src.categories.schemas import CreateCategorySchema
from tests.utils import create_category


async def test_category_create_success(ac: AsyncClient):
    response = await ac.post("/categories/", json={"name": "Medicine"})

    assert response.status_code == 200
    assert response.json()["name"] == "Medicine"
    assert response.json()["slug"] == "medicine"
    assert "id" in response.json()


async def test_category_create_fail(ac: AsyncClient):
    category_schema = CreateCategorySchema(name="Medicine")
    await create_category(category=category_schema)
    response = await ac.post("/categories/", json={"name": "Medicine"})

    assert response.status_code == 409
    assert response.json()["detail"] == "Object already exists."


# async def test_get_specific_operations(ac: AsyncClient):
#     response = await ac.get("/operations", params={
#         "operation_type": "Выплата купонов",
#     })

#     assert response.status_code == 200
#     assert response.json()["status"] == "success"
#     assert len(response.json()["data"]) == 1
