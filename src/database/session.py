from typing import AsyncGenerator
from src.core.settings import load_settings

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

settings = load_settings()
DATABASE_URL = settings.db_url

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    future=True,
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
