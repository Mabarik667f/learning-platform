from loguru import logger
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select
from tasks.shemas import CreateTask
from models.courses import Section as SectionModel, Subsection as SubSectionModel
from fastapi import status, HTTPException

from . import crud
from .shemas import CreateSection, CreateSubSection

"""Sections"""
async def get_selectin_section(
    session: AsyncSession,
    section_id: int
) -> SectionModel:
    q = (select(SectionModel)
        .where(SectionModel.id == section_id)
        .options(selectinload(SectionModel.subsections))
    )
    res = await session.execute(q)
    try:
        return res.scalar_one()
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"id": "Раздел не найден!"})


async def add_subsection_to_section(
    session: AsyncSession,
    section_id: int,
    subsection_for_create: CreateSubSection
) -> SectionModel:
    section_obj = await get_selectin_section(session, section_id)
    new_subsection = await crud.create_subsection(session, subsection_for_create)
    section_obj.subsections.append(new_subsection)

    await session.refresh(section_obj)
    await session.commit()
    return section_obj



async def bulk_create_section(
    session: AsyncSession,
    sections: list[CreateSection]
):
    pass


"""SubSections"""
async def get_selection_subsection(
    subsection_id: int,
    session: AsyncSession
) -> SubSectionModel:
    pass


async def add_task_to_subsection(
    session: AsyncSession,
    section_id: int,
    task_for_create: CreateTask
) -> SubSectionModel:
    pass
