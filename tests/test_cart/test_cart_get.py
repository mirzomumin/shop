from httpx import AsyncClient


# CART_SESSION_ID = {
#     'cart': {
#         '1': {
#             'product': {
#                 'id': 1,
#                 'name': 'Green Tea',
#                 'slug': 'green-tea',
#                 'image': 'media/images/image.jpg',
#                 'description': (
#                     "Lorem Ipsum is simply dummy text of the printing "
#                     "and typesetting industry. Lorem Ipsum has been the"
#                     " industry's standard dummy text ever since the 1500s,"
#                     " when an unknown printer took a galley of type and "
#                     "scrambled it to make a type specimen book."),
#                 'price': 109.99,
#                 'is_available': True,
#                 'category_id': 1,
#             },
#             'quantity': 2,
#             'price': 109.99,
#             'total_price': 219.98,
#         }
#     },
#     'cart_total_price': '219.9799999999999897681846051'
# }


async def test_get_empty_card_success(ac: AsyncClient):
    response = await ac.get("/cart/")

    response_data = response.json()
    assert response.status_code == 200
    assert response_data["cart"] == {}
    assert response_data["cart_total_price"] == "0"
