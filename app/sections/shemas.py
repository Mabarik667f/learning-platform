from pydantic import BaseModel, Field
from tasks.shemas import Task


class SectionBase(BaseModel):
    title: str
    describe: str
    position: int = Field(gt=0)


class UpdateSection(SectionBase):
    title: str = Field(default=None)
    describe: str = Field(default=None)
    position: int = Field(default=None, gt=0)


class CreateSection(SectionBase):
    course_id: int = 1
    subsections: list["SubSectionBase"] = Field(default=[])


class CreateSectionForCourseStruct(SectionBase):
    subsections: list["SubSectionBase"]


class SectionResponse(SectionBase):
    id: int
    course_id: int

    class Config:
        from_attributes = True


class SectionWithSubsectionsResponse(SectionResponse):
    subsections: list["SubSectionResponse"] = Field(default=[])


class SubSectionBase(BaseModel):
    title: str
    position: int


class UpdateSubSection(SubSectionBase):
    title: str = Field(default=None)
    position: int = Field(default=None)


class CreateSubSection(SubSectionBase):
    section_id: int = Field(gt=0)


class SubSectionResponse(SubSectionBase):
    id: int
    section_id: int = Field(gt=0)

    class Config:
        from_attributes = True


class SubSectionWithTasksResponse(SubSectionResponse):
    tasks: list["Task"] = Field(default=[])
