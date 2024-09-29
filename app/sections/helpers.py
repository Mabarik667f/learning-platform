from models.courses import Section as SectionModel
from .shemas import SubSectionResponse


def get_pydantic_subsections(section: SectionModel) -> list[SubSectionResponse]:
    return [SubSectionResponse(**sub.to_dict()) for sub in section.subsections]
