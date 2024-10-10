from enum import Enum
from typing import TYPE_CHECKING, List
from sqlalchemy import CheckConstraint, Integer, String, Enum as SqlEnum, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm.properties import ForeignKey
from sqlalchemy.sql.sqltypes import Text
from core.db import Base, pk
from datetime import datetime

if TYPE_CHECKING:
    from .categories import CourseHasCategory
    from .users import Cart, User


class Difficulty(str, Enum):
    EASY = ("easy",)
    MEDIUM = ("medium",)
    HARD = "hard"


class Course(Base):
    __tablename__ = "course"

    id: Mapped[pk]
    title: Mapped[str] = mapped_column(String(50))
    describe: Mapped[str | None] = mapped_column(Text, nullable=True)
    price: Mapped[int] = mapped_column(
        Integer, CheckConstraint("price >= 0"), nullable=False
    )
    img: Mapped[str] = mapped_column(String, nullable=False)
    difficulty: Mapped[Difficulty] = mapped_column(
        SqlEnum(Difficulty, name="difficulty_enum", create_type=False), nullable=False
    )

    categories: Mapped[List["CourseHasCategory"]] = relationship(
        back_populates="course"
    )
    users: Mapped[List["Cart"]] = relationship(back_populates="course")
    sections: Mapped[List["Section"]] = relationship(
        back_populates="course", lazy="selectin"
    )


class Section(Base):
    __tablename__ = "section"

    id: Mapped[pk]
    title: Mapped[str] = mapped_column(String(50))
    describe: Mapped[str | None] = mapped_column(Text, nullable=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("course.id", ondelete="CASCADE"))
    position: Mapped[int] = mapped_column(
        CheckConstraint("position > 0"), nullable=False
    )

    course: Mapped["Course"] = relationship(back_populates="sections")
    subsections: Mapped[List["Subsection"]] = relationship(
        back_populates="section", lazy="selectin"
    )


class Subsection(Base):
    __tablename__ = "subsection"

    id: Mapped[pk]
    title: Mapped[str] = mapped_column(String(50))
    position: Mapped[int] = mapped_column(
        CheckConstraint("position > 0"), nullable=False
    )
    section_id: Mapped[int] = mapped_column(
        ForeignKey("section.id", ondelete="CASCADE")
    )

    section: Mapped["Section"] = relationship(back_populates="subsections")
    tasks: Mapped[List["Task"]] = relationship(back_populates="subsection")


class Task(Base):
    __tablename__ = "task"

    id: Mapped[pk]
    text: Mapped[str | None] = mapped_column(Text, nullable=False)
    video_path: Mapped[str] = mapped_column(String, nullable=True)

    todo: Mapped[bool] = mapped_column(default=False)
    scores: Mapped[int] = mapped_column(CheckConstraint("scores > 0"), nullable=False)

    task_type_id: Mapped[int] = mapped_column(
        ForeignKey("task_type.id", ondelete="RESTRICT")
    )
    subsection_id: Mapped[int] = mapped_column(
        ForeignKey("subsection.id", ondelete="CASCADE")
    )

    subsection: Mapped["Subsection"] = relationship(back_populates="tasks")
    task_type: Mapped["TaskType"] = relationship(back_populates="tasks")

    answers: Mapped[list["Answer"]] = relationship(
        back_populates="task", lazy="selectin"
    )
    task_tests: Mapped[list["TaskTest"]] = relationship(
        back_populates="task", lazy="selectin"
    )
    submissions: Mapped[list["Submission"]] = relationship(back_populates="task")


class Answer(Base):
    __tablename__ = "answer"

    id: Mapped[pk]
    text: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_correct: Mapped[bool] = mapped_column(default=False)
    task_id: Mapped[int] = mapped_column(ForeignKey("task.id", ondelete="CASCADE"))

    task: Mapped["Task"] = relationship(back_populates="answers")


class TaskTest(Base):
    __tablename__ = "task_test"

    id: Mapped[pk]
    test_file: Mapped[str] = mapped_column(Text)

    task_id: Mapped[int] = mapped_column(ForeignKey("task.id", ondelete="CASCADE"))

    task: Mapped["Task"] = relationship(back_populates="task_tests")


class TaskType(Base):
    __tablename__ = "task_type"

    id: Mapped[pk]
    name: Mapped[str] = mapped_column(unique=True)

    tasks: Mapped[list["Task"]] = relationship(back_populates="task_type")


class Submission(Base):
    __tablename__ = "submission"

    submission_id: Mapped[pk]
    task_id: Mapped[int] = mapped_column(ForeignKey("task.id", ondelete="CASCADE"))
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user_account.id", ondelete="CASCADE")
    )

    submission_date: Mapped[str] = mapped_column(DateTime, default=datetime.utcnow)
    submission_code: Mapped[str] = mapped_column(Text)
    submission_answer: Mapped[str] = mapped_column(Text)

    user: Mapped["User"] = relationship(back_populates="submissions")
    task: Mapped["Task"] = relationship(back_populates="submissions")
