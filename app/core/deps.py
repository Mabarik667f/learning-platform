from typing import AsyncGenerator, Annotated
from fastapi.params import Depends
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from .db import async_engine

import categories.models
import courses.models
import users.models

async_session_maker = async_sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        try:
            yield session
        except:
            await session.rollback()
            raise
        finally:
            await session.close()


SessionDep = Annotated[AsyncSession, Depends(get_db)]
