from typing import Any, Annotated
from collections.abc import AsyncGenerator
from fastapi import UploadFile
from fastapi.params import Depends
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from .db import async_engine

from models import *

AsyncSessionMaker = async_sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionMaker() as session:
        try:
            yield session
        except:
            await session.rollback()
            raise
        finally:
            await session.close()


async def get_async_session_maker() -> (
    AsyncGenerator[async_sessionmaker[AsyncSession], Any]
):
    yield AsyncSessionMaker


SessionDep = Annotated[AsyncSession, Depends(get_db)]
AsyncSessionMakerDep = Annotated[async_sessionmaker, Depends(get_async_session_maker)]
