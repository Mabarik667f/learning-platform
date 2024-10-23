from fastapi.exceptions import HTTPException
from sqlalchemy import update, select, delete, or_
from fastapi import status
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio.session import AsyncSession
from models.users import User
from shemas.users import UserCreate

"""
Helpers
"""


async def user_in_db(session: AsyncSession, user: UserCreate) -> bool:
    q = select(User.email).where(
        or_(User.email == user.email, User.username == user.username)
    )
    result = await session.execute(statement=q)
    return bool(result.scalars().first())


async def get_user_by_id(session: AsyncSession, user_id) -> User:
    q = select(User).where(User.id == user_id)
    result = await session.execute(statement=q)
    res = result.scalar_one_or_none()
    if res:
        return res
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"id": "Такого пользователя не существует"},
        )


async def get_user_by_name(session: AsyncSession, username: str) -> User:
    q = select(User).where(User.username == username)
    result = await session.execute(statement=q)
    res = result.scalar_one_or_none()
    if res:
        return res
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"username": "Такого пользователя не существует"},
        )
