from fastapi import status
from fastapi.exceptions import HTTPException
from loguru import logger
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio.session import AsyncSession

from models.users import Profile, User
from users.shemas import UserAllData, UserCreate, UserUpdate
from users.utils import user_in_db, get_user_by_id
from auth.utils import get_password_hash

async def create_user(session: AsyncSession, user: UserCreate) -> User:
    user_exists = await user_in_db(session=session, user=user)

    if user_exists:
        raise HTTPException(detail={"email": "Пользователь с такой почтой или логином существует!"}, status_code=status.HTTP_400_BAD_REQUEST)

    async with session.begin_nested():

        password_hash = await get_password_hash(user.password)
        user_obj = User(
            username=user.username,
            email=user.email,
            hashed_password=password_hash,
            is_superuser=user.is_superuser,
            is_verified=user.is_verified,
            is_active=user.is_active,
            role=user.role.value
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

    for key, value in update_dict.items():
        setattr(user, key, value)

    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def delete_user(session: AsyncSession, user_id: int) -> None:
    user_obj = await get_user_by_id(session, user_id)

    user_data = user_obj.to_dict()
    user = UserAllData(**user_data)

    if user.is_superuser or user.role == 'owner':
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User is owner or superuser!")

    await session.delete(user_obj)
    await session.commit()
