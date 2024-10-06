from typing import Annotated, Any

from jwt import PyJWTError, InvalidTokenError, ExpiredSignatureError
from fastapi.exceptions import HTTPException
from fastapi.params import Depends
from fastapi.routing import APIRouter
from fastapi import BackgroundTasks, Response, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from .crud import create_auth_tokens, refresh_all_tokens
from .utils import auth_user, generate_activation_code
from .shemas import TokenRefresh, Tokens, VerifyCode
from mailings.tasks import send_mailing
from mailings.utils import MailingCodeUtils

from users.deps import CurActiveUserDep
from core.deps import SessionDep
from core.config import settings

from loguru import logger

router = APIRouter(prefix="/auth", tags=["auth"])


@router.patch("/code")
async def check_mail_code(
    session: SessionDep, code: VerifyCode, current_user: CurActiveUserDep
):
    true_code = MailingCodeUtils(current_user.username).check_code(code.code)
    if true_code:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    return Response(status_code=status.HTTP_400_BAD_REQUEST)


@router.post("/token")
async def login(
    session: SessionDep,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    background_tasks: BackgroundTasks,
) -> Tokens:

    user = await auth_user(session, form_data.username, form_data.password)

    access, refresh = await create_auth_tokens(
        data={"sub": form_data.username, "scopes": form_data.scopes},
    )

    activation_code = await generate_activation_code(user.username)
    background_tasks.add_task(
        send_mailing, user.email, msg=f"your activate code: {activation_code}"
    )
    return Tokens(access_token=access, refresh_token=refresh)


@router.post("/token/refresh")
async def refresh_token(
    refresh_token: TokenRefresh, current_user: CurActiveUserDep
) -> Tokens:
    try:
        access, refresh = await refresh_all_tokens(refresh_token)
        return Tokens(access_token=access, refresh_token=refresh)
    except (PyJWTError, InvalidTokenError, ExpiredSignatureError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid refresh token"
        )
