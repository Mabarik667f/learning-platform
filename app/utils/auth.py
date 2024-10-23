from datetime import timedelta, datetime, timezone
from random import randint
import jwt
from sqlalchemy.ext.asyncio.session import AsyncSession

from fastapi import status
from fastapi.exceptions import HTTPException

from core.config import settings
from models.users import User
from utils.users import get_user_by_name
from mailings.utils import MailingCodeUtils
from deps.auth import pwd_context

from loguru import logger


async def auth_user(session: AsyncSession, username: str, password: str) -> User:
    user = await get_user_by_name(session, username)
    if not await verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"password": "Неправильный логин или пароль"},
        )
    return user


async def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


async def get_password_hash(password: str):
    return pwd_context.hash(password)


async def generate_activation_code(username: str):
    code = "".join(str(randint(0, 9)) for _ in range(6))
    MailingCodeUtils(username).set_code(code)

    return code


async def create_jwt_token(data: dict, expires_delta: timedelta) -> str:
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = dict(exp=expire)
    to_encode.update(data)
    encoded_jwt = jwt.encode(
        payload=to_encode, key=settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt
