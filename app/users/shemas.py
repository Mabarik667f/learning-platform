from enum import Enum
from typing import List
from typing_extensions import Optional
from pydantic import BaseModel, EmailStr, Field

class RoleEnum(str, Enum):
    admin = "admin"
    user = "user"
    owner = "owner"

class User(BaseModel):
    username: str
    email: EmailStr
    role: RoleEnum = Field(default=RoleEnum.user)

class UserFlags(BaseModel):
    is_superuser: Optional[bool] = Field(default=False, exclude=True)
    is_verified: Optional[bool] = Field(default=False, exclude=True)
    is_active: Optional[bool] = Field(default=True, exclude=True)

class UserAllData(User, UserFlags):
    pass

class UserInDB(UserAllData):
    hashed_password: str


class UserCreate(UserAllData):
    password: str


class UserUpdate(UserAllData):
    pass


class UserResponse(UserAllData):
    id: int

    class Config:
        from_attributes = True


class Profile(BaseModel):
    user: User
