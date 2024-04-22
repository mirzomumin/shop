from httpx import AsyncClient


async def test_get_empty_card_success(ac: AsyncClient):
    response = await ac.get("/cart/")

    response_data = response.json()
    assert response.status_code == 200
    assert response_data["cart"] == {}
    assert response_data["cart_total_price"] == "0"
