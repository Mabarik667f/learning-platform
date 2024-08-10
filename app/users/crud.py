from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio.session import AsyncSession
from typing import Any

from users.models import Profile, User, Role
from users.shemas import UserAllData, UserCreate, UserUpdate
from users.utils import user_in_db, get_user_by_id, get_role_by_id, get_role_by_name
from auth.utils import get_password_hash

async def create_user(session: AsyncSession, user: UserCreate) -> User | HTTPException:
    user_exists = await user_in_db(session=session, user=user)

    if user_exists:
        raise HTTPException(detail="user exists!", status_code=status.HTTP_400_BAD_REQUEST)

    async with session.begin_nested():
        role = await session.execute(select(Role).filter_by(name=user.role))
        role = role.scalars().first()

        if not role:
            raise HTTPException(detail={"role": "invalid role!"}, status_code=status.HTTP_400_BAD_REQUEST)

        password_hash = await get_password_hash(user.password)

        user_obj = User(
            username=user.username,
            email=user.email,
            hashed_password=password_hash,
            is_superuser=user.is_superuser,
            is_verified=user.is_verified,
            is_active=user.is_active,
            role_id=role.id
        )

        session.add(user_obj)
        await session.flush()

        profile_obj = Profile(user_id=user_obj.id)
        session.add(profile_obj)

    await session.commit()
    await session.refresh(user_obj)

    return user_obj

async def update_user_data(session: AsyncSession, user_id: int, update_data: UserUpdate):

    user = await get_user_by_id(session, user_id)
    update_dict = update_data.dict(exclude_unset=True)

    if 'role' in update_dict:
        role_id = await get_role_by_name(session, update_dict['role'].value)
        update_dict['role_id'] = role_id
        del update_dict['role']

    for key, value in update_dict.items():
        setattr(user, key, value)

    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def delete_user(session: AsyncSession, user_id: int) -> None:
    user = await get_user_by_id(session, user_id)

    user_data = user.to_dict()
    user_data['role'] = await get_role_by_id(session, user_data['role_id'])
    user = UserAllData(**user_data)

    if user.is_superuser or user.role == 'owner':
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User is owner or superuser!")

    q = delete(User).where(User.id == user_id)
    await session.execute(q)
    await session.commit()


async def get_user_data(session: AsyncSession, user_id: int) -> dict[str, Any]:
    """Получение данных о пользователе в формате словаря"""
    user = await get_user_by_id(session, user_id)
    user_data = user.to_dict()
    user_data['role'] = await get_role_by_id(session, user_data['role_id'])
    return user_data
