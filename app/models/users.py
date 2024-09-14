from typing import TYPE_CHECKING, Optional, Annotated, List, get_args
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm.properties import ForeignKey
from sqlalchemy.util.typing import Literal
from sqlalchemy import Enum as SqlEnum
from enum import Enum

from core.db import Base, pk


if TYPE_CHECKING:
    from .courses import Course

class Role(str, Enum):
    OWNER = "OWNER"
    ADMIN = "ADMIN"
    USER = "USER"


class User(Base):
    __tablename__ = "user_account"

    id: Mapped[pk]
    username: Mapped[str]
    email: Mapped[str] = mapped_column(index=True, unique=True)
    hashed_password: Mapped[str]

    is_active: Mapped[Optional[bool]] = mapped_column(default=True, nullable=False)
    is_superuser: Mapped[Optional[bool]] = mapped_column(default=False, nullable=False)
    is_verified: Mapped[Optional[bool]] = mapped_column(default=False, nullable=False)
    role: Mapped[Role] = mapped_column(SqlEnum(Role, name="role_enum", create_type=False), nullable=False, default=Role.USER)

    profile: Mapped[Optional["Profile"]] = relationship(back_populates="user")
    courses: Mapped[list["Cart"]] = relationship(back_populates="user")


class Profile(Base):
    __tablename__ = "profile"

    id: Mapped[pk]
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id", ondelete="CASCADE"))

    user: Mapped["User"] = relationship(back_populates="profile")


class Cart(Base):
    __tablename__ = "cart"

    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id", ondelete="CASCADE"), primary_key=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("course.id", ondelete="CASCADE"), primary_key=True)
    is_selected: Mapped[bool] = mapped_column(default=False)

    user: Mapped["User"] = relationship(back_populates="courses")
    course: Mapped["Course"] = relationship(back_populates="users")
