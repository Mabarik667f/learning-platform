from random import randint
from sqlalchemy.ext.asyncio.session import AsyncSession

from fastapi import status
from fastapi.exceptions import HTTPException

from users.models import User
from users.utils import get_user_by_name
from mailings.utils import MailingCodeUtils
from .deps import pwd_context

async def auth_user(session: AsyncSession, username: str, password: str) -> User:
    user = await get_user_by_name(session, username)
    if not await verify_password(password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Неправильный логин или пароль")
    return user


async def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


async def get_password_hash(password: str):
    return pwd_context.hash(password)


async def generate_activation_code(username: str):
    code = ''.join(str(randint(0, 9)) for _ in range(6))
    MailingCodeUtils(username).set_code(code)

    return code
