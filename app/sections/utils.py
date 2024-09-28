from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select
from models.courses import Section as SectionModel
from .shemas import CreateSection
from fastapi import status, HTTPException

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
) -> SectionModel:
    pass


async def bulk_create_section(
    session: AsyncSession,
    sections: list[CreateSection]
):
    pass


"""SubSections"""
