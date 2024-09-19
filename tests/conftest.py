import asyncio
import pytest
from collections.abc import AsyncGenerator
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio.engine import create_async_engine
from sqlalchemy.ext.asyncio.session import AsyncSession, async_sessionmaker
import core
from core.db import Base
from core.config import settings
from main import app
from loguru import logger
from .helpers.auth_middleware import BearerAuth

async_engine = create_async_engine(str(settings.TEST_ASYNC_DB_URI))
async_session_maker = async_sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)

default_user_data: dict = {
    "email": "aboba@gmail.com",
    "username": "Test",
    "password": "+Password447",
    "password2": "+Password447",
    "scope": ["me"]}


async def connection() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        try:
            yield session
        except:
            raise
        finally:
            await session.rollback()
            await session.close()

app.dependency_overrides[core.deps.get_db] = connection

@pytest.fixture(scope="session", autouse=True)
async def setup():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture(scope="session")
def event_loop(request):
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="class")
async def create_user():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client: #type: ignore
        await client.post("/users/create-user", json=default_user_data)


@pytest.fixture
async def client():
    auth = BearerAuth(app, user=default_user_data)
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test", auth=auth) as client: #type: ignore
        yield client


@pytest.fixture(scope="class")
async def create_course(client: AsyncClient):
    pass
