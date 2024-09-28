from pydantic import BaseModel, Field
from tasks.shemas import Task

class SectionBase(BaseModel):
    title: str
    describe: str


class UpdateSection(SectionBase):
    title: str = Field(default="")
    describe: str = Field(default="")


class CreateSection(SectionBase):
    course_id: int = 1
    subsections: list['SubSectionBase'] = Field(default=[])


class SectionResponse(SectionBase):
    id: int
    course_id: int

    class Config:
        from_attributes = True

class SectionWithSubsectionsResponse(SectionResponse):
    subsections: list['SubSectionBase'] = Field(default=[])


class SubSectionBase(BaseModel):
    title: str


class UpdateSubSection(SubSectionBase):
    pass


class CreateSubSection(SubSectionBase):
    section_id: int = 1
    tasks: list['Task'] = Field(default=[])


class SubSectionResponse(SubSectionBase):
    id: int
    section_id: int = 1

    class Config:
        from_attributes = True

class SubSectionWithTasksResponse(SubSectionResponse):
    tasks: list['Task'] = Field(default=[])
