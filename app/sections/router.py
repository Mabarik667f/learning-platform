from fastapi import APIRouter, status, Response

from core.deps import SessionDep
from users.deps import CurActiveUserDep

from .shemas import (CreateSection, CreateSubSection,
    SectionResponse, SectionWithSubsectionsResponse,
    SubSectionResponse, SubSectionWithTasksResponse, UpdateSection, UpdateSubSection)
from .helpers import get_pydantic_subsections
from . import crud, utils

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
    created_section_obj = await crud.create_section(session, section)
    obj = await utils.get_selectin_section(session, created_section_obj.id)
    subsections = get_pydantic_subsections(obj)
    return SectionWithSubsectionsResponse(**obj.to_dict(), subsections=subsections)


@router_section.delete("/delete/{section_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_section(
    section_id: int,
    session: SessionDep,
    current_user: CurActiveUserDep,
):
    await crud.delete_section(session, section_id)


@router_section.patch("/patch/{section_id}", response_model=SectionResponse)
async def patch_section(
    section_id: int,
    updated_section: UpdateSection,
    current_user: CurActiveUserDep,
    session: SessionDep,
):
    """Change only section data, not added subsections this method!"""
    section_obj = await crud.patch_section(session, section_id, updated_section)
    return SectionResponse(**section_obj.to_dict())


@router_section.get("/{section_id}", response_model=SectionWithSubsectionsResponse)
async def get_section(
    section_id: int,
    session: SessionDep
):
    section_obj = await utils.get_selectin_section(session, section_id)
    subsections = get_pydantic_subsections(section_obj)
    return SectionWithSubsectionsResponse(**section_obj.to_dict(), subsections=subsections)


"""Other endpoints"""

@router_section.get("/list/{course_id}", response_model=list[SectionResponse])
async def get_list_sections(
    course_id: int,
    session: SessionDep
):
    section_objects = await crud.get_list_section(session, course_id)
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
    subsection_obj = await crud.create_subsection(session, subsection)
    return SubSectionWithTasksResponse(**subsection_obj.to_dict())


@router_subsection.delete("/delete/{subsection_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_subsection(
    session: SessionDep,
    current_user: CurActiveUserDep,
    subsection_id: int
):
    await crud.delete_subsection(session, subsection_id)

@router_subsection.patch("/patch/{subsection_id}", response_model=SubSectionResponse)
async def patch_subsection(
    session: SessionDep,
    current_user: CurActiveUserDep,
    subsection_id: int,
    updated_subsection: UpdateSubSection
):
    """Only scalars attributes patch"""
    obj = await crud.patch_subsection(session, subsection_id, updated_subsection)
    return SubSectionResponse(**obj.to_dict())

@router_subsection.get("/{subsection_id}", response_model=SubSectionWithTasksResponse)
async def get_subsection(
    subsection_id: int,
    session: SessionDep,
):
    # add tasks for response
    obj = await crud.get_subsection(session, subsection_id)
    return SubSectionWithTasksResponse(**obj.to_dict())

"""END CRUD"""

"""Other Endpoints"""
@router_subsection.get('/list/{section_id}', response_model=list[SubSectionResponse])
async def list_subsection(
    section_id: int,
    session: SessionDep,
):
    objects = await crud.get_list_subsection(session, section_id)
    return [SubSectionResponse(**s.to_dict()) for s in objects]
