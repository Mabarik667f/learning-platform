from pydantic import BaseModel
from typing import Optional


class Tokens(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenRefresh(BaseModel):
    refresh_token: str


class TokenData(BaseModel):
    username: Optional[str] = None
    pk: Optional[int] = None
    scopes: list[str] = []
    type: str = "access"


class VerifyCode(BaseModel):
    code: str
