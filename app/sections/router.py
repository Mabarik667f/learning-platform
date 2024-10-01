from fastapi import APIRouter, status, Response

from core.deps import SessionDep
from users.deps import CurActiveUserDep

from .shemas import (CreateSection, CreateSubSection,
    SectionResponse, SectionWithSubsectionsResponse,
    SubSectionResponse, SubSectionWithTasksResponse, UpdateSection, UpdateSubSection)
from .helpers import get_pydantic_subsections
from .crud import SectionCrud, SubSectionCrud

from loguru import logger

router_section = APIRouter(prefix="/sections", tags=["sections"])
router_subsection = APIRouter(prefix="/subsections", tags=["subsections"])

"""Sections"""

"""CRUD"""
@router_section.post("/create", response_model=SectionWithSubsectionsResponse, status_code=status.HTTP_201_CREATED)
async def create_section(
    section: CreateSection,
    current_user: CurActiveUserDep,
    session: SessionDep,
):
    """
    Base: create section object \n
    Params:\n
        subsections: any JSON objects\n
        example:\n
            {"title": "Test title", "describe": "Test describe"}\n
    """
    section_crud = SectionCrud(session)
    created_section_obj = await section_crud.create_section(section)
    obj = await section_crud.get_section(created_section_obj.id, load_selectin=True)
    subsections = get_pydantic_subsections(obj)
    return SectionWithSubsectionsResponse(**obj.to_dict(), subsections=subsections)


@router_section.delete("/delete/{section_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_section(
    section_id: int,
    session: SessionDep,
    current_user: CurActiveUserDep,
):
    await SectionCrud(session).delete_section(section_id)


@router_section.patch("/patch/{section_id}", response_model=SectionResponse)
async def patch_section(
    section_id: int,
    updated_section: UpdateSection,
    current_user: CurActiveUserDep,
    session: SessionDep,
):
    """Change only section data, not added subsections this method!"""
    section_crud = SectionCrud(session)
    section_obj = await section_crud.patch_section(section_id, updated_section)
    return SectionResponse(**section_obj.to_dict())


@router_section.get("/{section_id}", response_model=SectionWithSubsectionsResponse)
async def get_section(
    section_id: int,
    session: SessionDep
):
    section_obj = await SectionCrud(session).get_section(section_id, load_selectin=True)
    subsections = get_pydantic_subsections(section_obj)
    return SectionWithSubsectionsResponse(**section_obj.to_dict(), subsections=subsections)


"""Other endpoints"""

@router_section.get("/list/{course_id}", response_model=list[SectionResponse])
async def get_list_sections(
    course_id: int,
    session: SessionDep
):
    section_crud = SectionCrud(session)
    section_objects = await section_crud.get_list_section(course_id)
    return [SectionResponse(**s.to_dict()) for s in section_objects]


"""Subsections"""

"""CRUD"""

@router_subsection.post("/create", response_model=SubSectionResponse, status_code=status.HTTP_201_CREATED)
async def create_subsection(
    session: SessionDep,
    current_user: CurActiveUserDep,
    subsection: CreateSubSection
):
    """
    Base: create subsection object \n
    Params:
        tasks: any JSON objects
    """
    subsection_crud = SubSectionCrud(session)
    subsection_obj = await subsection_crud.create_subsection(subsection)
    return SubSectionWithTasksResponse(**subsection_obj.to_dict())


@router_subsection.delete("/delete/{subsection_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_subsection(
    session: SessionDep,
    current_user: CurActiveUserDep,
    subsection_id: int
):
    await SubSectionCrud(session).delete_subsection(subsection_id)

@router_subsection.patch("/patch/{subsection_id}", response_model=SubSectionResponse)
async def patch_subsection(
    session: SessionDep,
    current_user: CurActiveUserDep,
    subsection_id: int,
    updated_subsection: UpdateSubSection
):
    """Only scalars attributes patch"""

    subsection_crud = SubSectionCrud(session)
    obj = await subsection_crud.patch_subsection(subsection_id, updated_subsection)
    return SubSectionResponse(**obj.to_dict())

@router_subsection.get("/{subsection_id}", response_model=SubSectionWithTasksResponse)
async def get_subsection(
    subsection_id: int,
    session: SessionDep,
):
    # add tasks for response
    subsection_crud = SubSectionCrud(session)
    obj = await subsection_crud.get_subsection(subsection_id)
    return SubSectionWithTasksResponse(**obj.to_dict())


@router_subsection.get('/list/{section_id}', response_model=list[SubSectionResponse])
async def list_subsection(
    section_id: int,
    session: SessionDep,
):

    subsection_crud = SubSectionCrud(session)
    objects = await subsection_crud.get_list_subsection(section_id)
    return [SubSectionResponse(**s.to_dict()) for s in objects]

"""END CRUD"""
