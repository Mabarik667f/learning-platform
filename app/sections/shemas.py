from pydantic import BaseModel


class SectionBase(BaseModel):
    title: str
    describe: str

    subsections: list['SubSection']


class UpdateSection(SectionBase):
    pass


class CreateSection(SectionBase):
    course_id: int


class Section(SectionBase):
    id: int
    course_id: int

    class Config:
        from_attributes = True



class SubSectionBase(BaseModel):
    title: str
    number: int
    # add content

class UpdateSubSection(SubSectionBase):
    pass


class CreateSubSection(SubSectionBase):
    section_id: int


class SubSection(SectionBase):
    id: int
    section_id: int

    class Config:
        from_attributes = True
