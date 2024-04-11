from fastapi import FastAPI

from src.categories.router import router as categories_router
from src.products.router import router as products_router


app = FastAPI()


app.include_router(categories_router, prefix="/categories", tags=["categories"])
app.include_router(products_router, prefix="/products", tags=["products"])
