from enum import Enum
from typing import TYPE_CHECKING, List
from sqlalchemy import CheckConstraint, Integer, String, Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm.properties import ForeignKey
from sqlalchemy.sql.sqltypes import Text
from core.db import Base, pk

if TYPE_CHECKING:
    from categories.models import CourseHasCategory

class Difficulty(Enum):
    EASY = 'easy',
    MEDIUM = "medium",
    HARD = "hard"

class Course(Base):
    __tablename__ = "course"

    id: Mapped[pk]
    name: Mapped[str] = mapped_column(String(50))
    text: Mapped[str | None] = mapped_column(Text, nullable=True)
    price: Mapped[int] = mapped_column(Integer, CheckConstraint("price >= 0"), nullable=False)
    img: Mapped[str] = mapped_column(String, nullable=False)
    difficulty: Mapped[Difficulty] = mapped_column(SqlEnum(Difficulty, name="difficulty_enum", create_type=False),
        nullable=False)

    categories: Mapped[List["CourseHasCategory"]] = relationship(back_populates="course")
    sections: Mapped[List["Section"]] = relationship(back_populates="course")

class Section(Base):
    __tablename__ = "section"

    id: Mapped[pk]
    title: Mapped[str] = mapped_column(String(50))
    text: Mapped[str | None] = mapped_column(Text, nullable=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("course.id", ondelete="CASCADE"))

    course: Mapped["Course"] = relationship(back_populates="sections")
    subsections: Mapped[List["Subsection"]] = relationship(back_populates="section")

class Subsection(Base):
    __tablename__ = "subsection"

    id: Mapped[pk]
    title: Mapped[str] = mapped_column(String(50))
    number: Mapped[int]
    section_id: Mapped[int] = mapped_column(ForeignKey("section.id", ondelete="CASCADE"))

    section: Mapped["Section"] = relationship(back_populates="subsections")
    content_sections: Mapped[List['ContentSection']] = relationship(back_populates="subsection")


class ContentSection(Base):
    __tablename__ = "content_section"

    id: Mapped[pk]
    text: Mapped[str | None] = mapped_column(Text, nullable=True)
    video: Mapped[str] = mapped_column(String, nullable=False)
    subsection_id: Mapped[int] = mapped_column(ForeignKey("subsection.id", ondelete="CASCADE"))

    subsection: Mapped["Subsection"] = relationship(back_populates="content_sections")
    questions: Mapped[List["Question"]] = relationship(back_populates="content_section")

class Question(Base):
    __tablename__ = "question"

    id: Mapped[pk]
    text: Mapped[str] = mapped_column(Text)
    content_section_id: Mapped[int] = mapped_column(ForeignKey("content_section.id", ondelete="CASCADE"))

    content_section: Mapped["ContentSection"] = relationship(back_populates="questions")
    answers: Mapped[List["Answer"]] = relationship(back_populates="question")

class Answer(Base):
    __tablename__ = "answer"

    id: Mapped[pk]
    text: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_correct: Mapped[bool] = mapped_column(default=False)
    question_id: Mapped[int] = mapped_column(ForeignKey("question.id", ondelete="CASCADE"))

    question: Mapped["Question"] = relationship(back_populates="answers")
