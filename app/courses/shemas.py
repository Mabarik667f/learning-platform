from pydantic.fields import Field
from pydantic.main import BaseModel
from pydantic.types import PositiveInt

from categories.shemas import Category
from sections.shemas import Section
from courses.models import Difficulty

class CourseBase(BaseModel):
    title: str
    describe: str | None = None
    img: str
    price: PositiveInt
    difficulty: Difficulty = Field(default=Difficulty.EASY)


class CreateCourse(CourseBase):
    categories: list[int]


class UpdateCourse(CourseBase):
    pass


class AddCategoriesToCourse(BaseModel):
    category_ids: list[int]


class CourseWithCategories(CourseBase):
    categories: list[Category]


class CourseResponse(CourseBase):
    id: int

    class Config:
        from_attributes = True

class CourseAllData(CourseResponse):
    categories: list[Category]
    sections: list[Section] | None = None


class CourseListQueryParams(BaseModel):
    difficulties: list[Difficulty] | None = None
    min_price: int | None = None
    max_price: int | None = None
    categories: list[int] | None = None


class CourseDifficulty(BaseModel):
    title: Difficulty | str
