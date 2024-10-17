from pydantic import FilePath
from pydantic.fields import Field
from fastapi import Form
from pydantic.main import BaseModel
from pydantic.types import PositiveInt

from categories.shemas import Category, CategoryResponse
from sections.shemas import (
    CreateSectionForCourseStruct,
    SectionBase,
    SectionWithSubsectionsResponse,
)
from models.courses import Difficulty


class CourseBase(BaseModel):
    title: str
    describe: str | None = None
    img: FilePath | None = None
    price: PositiveInt
    difficulty: Difficulty = Field(default=Difficulty.EASY)


class CreateCourse(CourseBase):
    categories: list[int] = [1]

    @classmethod
    def as_form(
        cls,
        title: str = Form(...),
        describe: str | None = Form(None),
        price: PositiveInt = Form(...),
        difficulty: str = Form(Difficulty.EASY),
        categories: list[int] = Form(...)
    ):
        return cls(
            title=title,
            describe=describe,
            price=price,
            difficulty=Difficulty(difficulty),
            categories=categories
        )


class UpdateCourse(CourseBase):
    pass

    @classmethod
    def as_form(
        cls,
        title: str = Form(...),
        describe: str | None = Form(None),
        price: PositiveInt = Form(...),
        difficulty: str = Form(Difficulty.EASY),
    ):
        return cls(
            title=title,
            describe=describe,
            price=price,
            difficulty=Difficulty(difficulty),
        )

class AddCategoriesToCourse(BaseModel):
    category_ids: list[int] = [1]


class CourseWithCategories(CourseBase):
    categories: list[Category]


class CourseResponse(CourseBase):
    id: int

    class Config:
        from_attributes = True


class CourseAllData(CourseResponse):
    categories: list[CategoryResponse]
    sections: list["SectionWithSubsectionsResponse"] | None = None


class CourseListQueryParams(BaseModel):
    difficulties: list[Difficulty] | None = None
    min_price: int | None = None
    max_price: int | None = None
    categories: list[int] | None = None


class CourseDifficulty(BaseModel):
    title: Difficulty | str


class CreateCourseStruct(BaseModel):
    sections: list["CreateSectionForCourseStruct"]
