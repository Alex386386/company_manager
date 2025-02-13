from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from common_models.config import settings

database_url = URL.create(
    drivername=settings.db_engine,
    username=settings.postgres_user,
    password=settings.postgres_password,
    host=settings.db_host,
    port=settings.db_port,
    database=settings.db_name,
)

async_engine = create_async_engine(database_url, future=True)

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine, autoflush=False, expire_on_commit=False, autocommit=False
)


async def get_async_session():
    async with AsyncSessionLocal() as async_session:
        yield async_session
