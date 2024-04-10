from fastapi import FastAPI

from src.categories.router import router as categories_router


app = FastAPI()


app.include_router(categories_router, prefix="/categories", tags=["categories"])
