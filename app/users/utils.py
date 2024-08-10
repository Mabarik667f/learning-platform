from fastapi.exceptions import HTTPException
from sqlalchemy import update, select, delete, or_
from fastapi import status
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio.session import AsyncSession
from users.models import User, Role
from users.shemas import UserCreate

"""
Helpers
"""


async def user_in_db(session: AsyncSession, user: UserCreate) -> bool:
    q = select(User.email).where(or_(User.email == user.email, User.username == user.username))
    result = await session.execute(statement=q)
    return bool(result.scalars().first())


async def get_user_by_id(session: AsyncSession, user_id) -> User:
    q = (
        select(User)
        .where(User.id == user_id)
    )
    result = await session.execute(statement=q)
    res = result.scalar_one_or_none()
    if res:
        return res
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")


async def get_user_by_name(session: AsyncSession, username: str) -> User:
    q = (
        select(User)
        .where(User.username == username)
    )
    result = await session.execute(statement=q)
    res = result.scalar_one_or_none()
    if res:
        return res
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")


async def get_role_by_name(session: AsyncSession, role_name: str) -> int:
    q = select(Role.id).where(Role.name == role_name)
    try:
        res = await session.execute(q)
        val = res.scalars().one()
        return val
    except NoResultFound:
        raise HTTPException(status_code=status.http_400_bad_request, detail="Role not found")


async def get_role_by_id(session: AsyncSession, role_id: int) -> str:
    q = select(Role.name).where(Role.id == role_id)
    try:
        res = await session.execute(q)
        val = res.scalars().one()
        return val
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
