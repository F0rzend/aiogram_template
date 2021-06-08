from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import registry
from sqlalchemy.orm import sessionmaker, DeclarativeMeta

mapper_registry = registry()


class Base(metaclass=DeclarativeMeta):
    """ Declarative meta for mypy """
    __abstract__ = True
    __mapper_args__ = {"eager_defaults": True}

    # these are supplied by the sqlalchemy-stubs or sqlalchemy2-stubs, so may be omitted
    # when they are installed
    registry = mapper_registry
    metadata = mapper_registry.metadata


async def create_pool(
        connection_uri: str = "postgresql+asyncpg://postgres:postgres@localhost/postgres",
):
    engine = create_async_engine(url=make_url(connection_uri))
    pool = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False, autoflush=False)
    return pool

