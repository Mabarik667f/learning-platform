import jwt
from fastapi.params import Security
from jwt.exceptions import InvalidTokenError

from fastapi import Depends, status
from fastapi.security.oauth2 import SecurityScopes
from typing import Annotated
from loguru import logger

from datetime import timedelta, datetime, timezone

from starlette.exceptions import HTTPException
from core.deps import SessionDep
from core.config import settings
from .shemas import TokenData
from .deps import OAuth2Dep

from users.models import User
from users.utils import get_user_by_name
from users.shemas import UserResponse

from pydantic import ValidationError


async def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


async def get_current_user(
    session: SessionDep,
    security_scopes: SecurityScopes = SecurityScopes(),
    token: str = OAuth2Dep
) -> UserResponse | HTTPException | None:

    if security_scopes.scopes:
        auth_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        auth_value = "Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": auth_value},
    )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get('sub')
        if username is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, username=username)
    except (InvalidTokenError, ValidationError):
        raise credentials_exception

    user = await get_user_by_name(session, username)

    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": auth_value},
            )

    if isinstance(user, User):
        return UserResponse(
            **user.to_dict()
        )

async def get_current_active_user(
    current_user: Annotated[UserResponse, Security(get_current_user, scopes=["me"])]
) -> UserResponse:
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return current_user
