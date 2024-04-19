from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from src.config import settings
from src.categories.router import router as categories_router
from src.products.router import router as products_router
from src.cart.router import router as cart_router


app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=settings.CART_SESSION_ID)


app.include_router(categories_router, prefix="/categories", tags=["categories"])
app.include_router(products_router, prefix="/products", tags=["products"])
app.include_router(cart_router, prefix="/cart", tags=["cart"])
