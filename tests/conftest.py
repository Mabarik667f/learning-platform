import asyncio
import pytest

from typing import Any
from collections.abc import AsyncGenerator
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio.engine import create_async_engine
from sqlalchemy.ext.asyncio.session import AsyncSession, async_sessionmaker

import core #type: ignore

from core.db import Base #type: ignore
from core.config import settings #type: ignore
from main import app #type: ignore
from .helpers.auth_middleware import BearerAuth, get_auth_header

from loguru import logger

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


async def get_async_session_maker_test() -> AsyncGenerator[async_sessionmaker[AsyncSession], Any]:
    yield async_session_maker

app.dependency_overrides[core.deps.get_db] = connection
app.dependency_overrides[core.deps.get_async_session_maker] = get_async_session_maker_test

@pytest.fixture(scope="module", autouse=True)
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


@pytest.fixture(scope="module")
async def create_user():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client: #type: ignore
        await client.post("/users/create-user", json=default_user_data)

@pytest.fixture(scope="module")
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client: #type: ignore
        yield client

@pytest.fixture(scope="module")
async def token(client):
    auth = BearerAuth(app, user=default_user_data)
    yield await auth.async_get_token()


@pytest.fixture()
async def create_categories(client: AsyncClient, token: str):
    categories = ["Python", "Rust", "Algorithms"]
    for cat in categories:
        await client.post("/categories/create", json={"title": cat}, headers=get_auth_header(token))


@pytest.fixture
async def create_course(client: AsyncClient, create_categories, token: str):
    data = {
      "title": "string",
      "describe": "string",
      "img": "string",
      "price": 1,
      "difficulty": "easy",
      "categories": [1]
    }
    await client.post("/courses/create", json=data, headers=get_auth_header(token))


@pytest.fixture
async def create_section(client: AsyncClient, create_course, token: str):
    data = {"title": "Test section 1", "describe": "this section test 1",
        "course_id": 1, "subsections": [], "position": 1}
    await client.post("/sections/create", json=data, headers=get_auth_header(token))
