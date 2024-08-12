from typing import Optional, Annotated, List, get_args

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm.properties import ForeignKey
from sqlalchemy.sql.sqltypes import Enum
from sqlalchemy.util.typing import Literal
from sqlalchemy import BigInteger, Identity

from core.db import Base

pk = Annotated[int, mapped_column(BigInteger, Identity(), primary_key=True)]
Roles =  Literal["owner", "admin", "user"]


class User(Base):
    __tablename__ = "user_account"

    id: Mapped[pk]
    username: Mapped[str]
    email: Mapped[str] = mapped_column(index=True, unique=True)
    hashed_password: Mapped[str]

    is_active: Mapped[Optional[bool]] = mapped_column(default=True, nullable=False)
    is_superuser: Mapped[Optional[bool]] = mapped_column(default=False, nullable=False)
    is_verified: Mapped[Optional[bool]] = mapped_column(default=False, nullable=False)
    role_id: Mapped[int] = mapped_column(ForeignKey("role.id", ondelete="SET NULL"))

    role: Mapped[Optional["Role"]] = relationship(back_populates="users")
    profile: Mapped[Optional["Profile"]] = relationship(back_populates="user")


class Profile(Base):
    __tablename__ = "profile"

    id: Mapped[pk]
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id", ondelete="CASCADE"))

    user: Mapped["User"] = relationship(back_populates="profile")


class Role(Base):
    __tablename__ = "role"

    id: Mapped[pk]
    name: Mapped[Roles] = mapped_column(Enum(*get_args(Roles),
        name="roles",
        create_constraint=True,
        validate_strings=True
    ))

    users: Mapped[List["User"]] = relationship("User", back_populates="role")
