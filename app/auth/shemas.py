from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
    pk: Optional[int] = None
    scopes: list[str] = []


class VerifyCode(BaseModel):
    code: str
