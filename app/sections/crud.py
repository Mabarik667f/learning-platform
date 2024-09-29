import asyncio
from collections.abc import Sequence
from typing import NoReturn
from sqlalchemy import delete, select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio.session import AsyncSession
from fastapi import HTTPException, status
from sqlalchemy.orm import selectinload

from models.courses import Section as SectionModel, Subsection as SubSectionModel
from courses.crud import get_course
from .shemas import CreateSection, CreateSubSection, UpdateSection, UpdateSubSection
from .utils import get_selectin_section

from loguru import logger

"""Sections"""
async def create_section(
    session: AsyncSession,
    section: CreateSection
) -> SectionModel:

    await get_course(session, section.course_id)

    section_dict = section.dict()
    subsections = section_dict.pop('subsections', [])

    section_obj = SectionModel(**section_dict)
    if subsections:
        logger.info(subsections)
        subs = await asyncio.gather(*
            [create_subsection(session, CreateSubSection(**sub)) for sub in subsections]
        )
        section_obj.subsections.extend(subs)

    session.add(section_obj)

    await session.commit()
    await session.refresh(section_obj)
    return section_obj


async def delete_section(
    session: AsyncSession,
    section_id: int
) -> NoReturn:
    section_obj = await get_selectin_section(session, section_id)
    subssection_ids: list[int] = [s.id for s in section_obj.subsections]
    del_q = (delete(SubSectionModel)
        .where(SubSectionModel.id.in_(subssection_ids)))

    await session.execute(del_q)
    await session.delete(section_obj)
    await session.commit()


async def patch_section(
    session: AsyncSession,
    section_id: int,
    section: UpdateSection
) -> SectionModel:
    section_obj = await get_section(session, section_id)
    for key, val in section.dict().items():
        if section.dict().get(key, ""):
            setattr(section_obj, key, val)

    await session.commit()
    await session.refresh(section_obj)

    return section_obj


async def get_section(
    session: AsyncSession,
    section_id: int
) -> SectionModel:
    q = select(SectionModel).where(SectionModel.id == section_id)
    res = await session.execute(q)
    try:
        return res.scalar_one()
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"id": "Раздел не найден!"})


async def get_list_section(
    session: AsyncSession,
    course_id: int
) -> Sequence[SectionModel]:
    q = select(SectionModel).where(SectionModel.course_id == course_id)

    res = await session.execute(q)
    return res.scalars().all()


"""SubSections"""
async def create_subsection(
    session: AsyncSession,
    subsection: CreateSubSection
) -> SubSectionModel:
    await get_section(session, subsection.section_id)
    subsection_dict = subsection.dict()
    tasks = subsection_dict.pop('tasks')
    if tasks:
        pass

    subsection_obj = SubSectionModel(**subsection_dict)
    session.add(subsection_obj)

    await session.commit()
    await session.refresh(subsection_obj)
    return subsection_obj


async def delete_subsection(
    session: AsyncSession,
    subsection_id: int
) -> NoReturn:
    subsection_obj = await get_subsection(session, subsection_id)
    await session.delete(subsection_obj)
    await session.commit()


async def patch_subsection(
    session: AsyncSession,
    subsection_id: int,
    updated_subsection: UpdateSubSection
) -> SubSectionModel:
    subsection_obj = await get_subsection(session, subsection_id)
    for key, val in updated_subsection.dict().items():
        setattr(subsection_obj, key, val)

    await session.commit()
    await session.refresh(subsection_obj)
    return subsection_obj


async def get_subsection(
    session: AsyncSession,
    subsection_id: int
) -> SubSectionModel:
    q = select(SubSectionModel).where(SubSectionModel.id == subsection_id)
    res = await session.execute(q)
    try:
        return res.scalar_one()
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"id": "Подраздел не найден!"})


async def get_list_subsection(
    session: AsyncSession,
    section_id: int
) -> Sequence[SubSectionModel]:
    await get_section(session, section_id)
    q = select(SubSectionModel).where(SubSectionModel.section_id == section_id)

    res = await session.execute(q)
    return res.scalars().all()
