from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


async def create_pool(
    connection_uri: str = "postgresql+asyncpg://postgres:postgres@localhost/postgres",
):
    engine = create_async_engine(url=make_url(connection_uri))
    pool = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False, autoflush=False)
    return pool
