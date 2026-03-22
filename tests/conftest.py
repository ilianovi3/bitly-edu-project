from dotenv import load_dotenv
load_dotenv(".test.env", override=True)

import pytest
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
    AsyncEngine
)
from collections.abc import AsyncGenerator
from httpx import AsyncClient, ASGITransport

from app.main import app
from app.core.dependencies import get_db
from app.core.database import Base
from app.core.config import get_settings


settings = get_settings()

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture
def engine() -> AsyncEngine:
    # Новый engine для каждого теста — решает проблему с event loop
    return create_async_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
    )

@pytest.fixture
async def db_session(engine) -> AsyncGenerator[AsyncSession, None]:
    TestSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)
    async with TestSessionLocal() as session:
        try:
            yield session
            await session.rollback()
        finally:
            await session.close()


@pytest.fixture(autouse=True)  # scope="function" по умолчанию
async def setup_db(engine) -> AsyncGenerator[None, None]:
    assert settings.IS_TEST
    async with engine.connect() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await conn.commit()
    yield
    async with engine.connect() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def client(engine) -> AsyncGenerator[AsyncClient, None]:
    async def override_db():
        TestSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)
        async with TestSessionLocal() as session:
            try:
                yield session
                await session.rollback()
            finally:
                await session.close()

    app.dependency_overrides[get_db] = override_db
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac
    app.dependency_overrides.clear()
