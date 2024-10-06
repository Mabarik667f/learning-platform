from enum import Enum
import re
from typing import List
from typing_extensions import Optional
from pydantic import BaseModel, EmailStr, Field, validator
from core.exceptions import CoreValidationError


class RoleEnum(str, Enum):
    admin = "ADMIN"
    user = "USER"
    owner = "OWNER"


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
    password: str = Field(examples=["+Password447"])

    @validator("password", always=True)
    def validate_password(cls, password):
        pattern = r"^[a-zA-Z0-9!@#$%^&*()_+\-={}\[\]:;,.<>/?|\\]+$"

        if not any(c.islower() for c in password):
            raise CoreValidationError(
                "password",
                "Пароль должен содержать хотя бы одну букву нижнего регистра",
            )

        if not any(c.isupper() for c in password):
            raise CoreValidationError(
                "password",
                "Пароль должен содержать хотя бы одну букву верхнего регистра",
            )

        if not any(c.isdigit() for c in password):
            raise CoreValidationError(
                "password", "Пароль должен содержать хотя бы одну цифру"
            )

        if not re.match(pattern, password):
            raise CoreValidationError(
                "password", "Пароль содержит недопустимые символы"
            )

        return password


class UserUpdate(UserAllData):
    pass


class UserResponse(UserAllData):
    id: int

    class Config:
        from_attributes = True


class Profile(BaseModel):
    user: User


class Cart(BaseModel):
    pass
