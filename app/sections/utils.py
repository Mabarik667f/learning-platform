from loguru import logger
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select
from tasks.shemas import CreateTask
from models.courses import Section as SectionModel, Subsection as SubSectionModel
from fastapi import status, HTTPException

from .crud import SectionCrud, SubSectionCrud
from .shemas import CreateSection, CreateSubSection

"""Sections"""

async def add_subsection_to_section(
    session: AsyncSession,
    section_id: int,
    subsection_for_create: CreateSubSection
) -> SectionModel:

    section_obj = await SectionCrud(session).get_section(section_id, load_selectin=True)
    new_subsection = await SubSectionCrud(session).create_subsection(subsection_for_create)
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
