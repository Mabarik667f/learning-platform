from datetime import timedelta
from typing import Annotated, Any

from fastapi.exceptions import HTTPException
from fastapi.params import Depends
from fastapi.routing import APIRouter
from fastapi import BackgroundTasks, Response, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from .crud import create_access_token
from .utils import auth_user, generate_activation_code
from .shemas import Token, VerifyCode
from mailings.tasks import send_mailing
from mailings.utils import MailingCodeUtils

from users.deps import CurActiveUserDep
from core.deps import SessionDep
from core.config import settings

from loguru import logger

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

@router.patch("/code")
async def check_mail_code(session: SessionDep, code: VerifyCode, current_user: CurActiveUserDep):
    true_code = MailingCodeUtils(current_user.username).check_code(code.code)
    if true_code:
       return Response(status_code=status.HTTP_204_NO_CONTENT)
    return Response(status_code=status.HTTP_400_BAD_REQUEST)


@router.post('/token')
async def login(
    session: SessionDep,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    background_tasks: BackgroundTasks) -> Token:

    user = await auth_user(session, form_data.username, form_data.password)

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await create_access_token(
        data={"sub": form_data.username, "scopes": form_data.scopes},
        expires_delta=access_token_expires
    )

    activation_code = await generate_activation_code(user.username)
    background_tasks.add_task(send_mailing, user.email, msg=f"your activate code: {activation_code}")
    return Token(access_token=access_token, token_type="bearer")
