import jwt
from fastapi.params import Security
from jwt.exceptions import InvalidTokenError, PyJWTError

from fastapi import Depends, status
from fastapi.security.oauth2 import SecurityScopes
from typing import Annotated
from loguru import logger

from datetime import timedelta, datetime, timezone

from starlette.exceptions import HTTPException
from core.deps import SessionDep
from core.config import settings
from utils.auth import create_jwt_token
from shemas.auth import TokenData, TokenRefresh
from deps.auth import OAuth2Dep

from models.users import User
from utils.users import get_user_by_name
from shemas.users import UserResponse

from pydantic import ValidationError


async def create_auth_tokens(data: dict) -> tuple[str, str]:
    access_token_expire = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expire = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    refresh_data = dict(type="refresh")
    refresh_data.update(data)

    access = await create_jwt_token(data=data, expires_delta=access_token_expire)
    refresh = await create_jwt_token(
        data=refresh_data, expires_delta=refresh_token_expire
    )

    return access, refresh


async def get_current_user(
    session: SessionDep,
    security_scopes: SecurityScopes = SecurityScopes(),
    token: str = OAuth2Dep,
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
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
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
        return UserResponse(**user.to_dict())


async def get_current_active_user(
    current_user: Annotated[UserResponse, Security(get_current_user, scopes=["me"])]
) -> UserResponse:
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
    return current_user


async def refresh_all_tokens(refresh_token: TokenRefresh) -> tuple[str, str]:
    """Можно сделать blacklist для refresh"""
    payload = jwt.decode(
        refresh_token.refresh_token,
        settings.SECRET_KEY,
        algorithms=[settings.ALGORITHM],
    )
    username: str = payload.get("sub")

    if username is None or payload.get("type") != "refresh":
        raise PyJWTError

    token_scopes = payload.get("scopes")
    data = TokenData(username=username, scopes=token_scopes)
    access, refresh = await create_auth_tokens(data=data.dict())
    return access, refresh
