from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase


SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://admin:admin@localhost/shop_db"

async_engine = create_async_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=async_engine)


class Base(DeclarativeBase, AsyncAttrs):
    pass


async def get_db() -> AsyncGenerator:
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()
