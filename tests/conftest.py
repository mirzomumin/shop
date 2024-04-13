# import asyncpg
# import pytest

# from sqlalchemy.ext.asyncio import create_async_engine
# from src.database import Base
# from src.config import settings

# SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}/test_{settings.DB_NAME}"

# async_engine = create_async_engine(SQLALCHEMY_DATABASE_URL)


# @pytest.fixture(autouse=True, scope='session')
# async def test_db():
#     dsn='postgresql://'\
#             f'{settings.DB_USER}:{settings.DB_PASS}'\
#             f'@{settings.DB_HOST}:{settings.DB_PORT}/postgres'
#     try:
#         connect = await asyncpg.connect(dsn)
#         connect.autocommit = True
#         curs = await connect.cursor() # cursor

#         # Create test database and tables
#         await curs.execute(f'CREATE DATABASE test_{settings.DB_NAME} '
#                         f'OWNER {settings.DB_USER}')
#         await Base.metadata.create_all(bind=async_engine)

#         # Run tests
#         yield

#         # Drop test database and tables
#         await Base.metadata.drop_all(bind=async_engine)
#         await curs.execute(f'DROP DATABASE test_{settings.DB_NAME}')
#         print('DROP TEST DATABASE')
#     finally:
#         connect.close()
