from typing import List, TYPE_CHECKING, Optional
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.db import Base, pk

if TYPE_CHECKING:
    from courses.models import *

class Category(Base):
    __tablename__ = "category"

    id: Mapped[pk]
    title: Mapped[str] = mapped_column(String(50), unique=True)
    slug: Mapped[str] = mapped_column(unique=True, index=True)

    courses: Mapped[Optional[List["CourseHasCategory"]]] = relationship(back_populates="category")


class CourseHasCategory(Base):
    __tablename__ = "course_has_category"

    category_id: Mapped[int] = mapped_column(ForeignKey("category.id", ondelete="CASCADE"), primary_key=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("course.id", ondelete="CASCADE"), primary_key=True)

    category: Mapped["Category"] = relationship(back_populates="courses")
    course: Mapped["Course"] = relationship(back_populates="categories")
