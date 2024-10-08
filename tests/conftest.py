import asyncio
import pytest

from typing import Any
from collections.abc import AsyncGenerator
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio.engine import create_async_engine
from sqlalchemy.ext.asyncio.session import AsyncSession, async_sessionmaker

import core  # type: ignore

from core.db import Base  # type: ignore
from core.config import settings  # type: ignore
from main import app  # type: ignore
from tests.fixtures.api import *
from tests.fixtures.auth import *

from loguru import logger

async_engine = create_async_engine(str(settings.TEST_ASYNC_DB_URI))
async_session_maker = async_sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)


async def connection() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        try:
            yield session
        except:
            raise
        finally:
            await session.rollback()
            await session.close()


async def get_async_session_maker_test() -> (
    AsyncGenerator[async_sessionmaker[AsyncSession], Any]
):
    yield async_session_maker


app.dependency_overrides[core.deps.get_db] = connection
app.dependency_overrides[core.deps.get_async_session_maker] = (
    get_async_session_maker_test
)


@pytest.fixture(autouse=True)
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


@pytest.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:  # type: ignore
        yield client
