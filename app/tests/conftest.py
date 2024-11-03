import asyncio
from importlib import reload
from pathlib import Path
import shutil
import pytest
import os

from typing import Any
from collections.abc import AsyncGenerator
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy.ext.asyncio.engine import create_async_engine
from sqlalchemy.ext.asyncio.session import AsyncSession, async_sessionmaker

import core
from app import BASE_PATH
from core.db import Base
from core.config import settings
from main import app
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
        await start_all_sql_fixtures(conn)
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

    clear_test_media()


@pytest.fixture
async def client():
    async with app.router.lifespan_context(app):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:  # type: ignore
            yield client


@pytest.fixture
async def session() -> AsyncGenerator[AsyncSession, None]:
    async for conn in connection():
        yield conn


async def start_all_sql_fixtures(conn: AsyncConnection):
    """read all SQL FILES from sql_scripts and make it"""
    sql_scripts = os.path.relpath(f"{BASE_PATH}/migrations/sql_scripts")
    for f in os.listdir(sql_scripts):
        await execute_sql_script(f, conn)


async def execute_sql_script(filename: str, connection: AsyncConnection):
    path = Path(f"{BASE_PATH}/migrations/sql_scripts/{filename}")
    with open(path, "r") as f:
        await connection.execute(text(f.read()))


def clear_test_media():
    shutil.rmtree("test_dir/")


@pytest.fixture(autouse=True)
def monkeypatch_media_path(monkeypatch: pytest.MonkeyPatch):
    test_dir = Path("test_dir/")
    test_dir.mkdir(exist_ok=True)
    monkeypatch.chdir("test_dir/")
