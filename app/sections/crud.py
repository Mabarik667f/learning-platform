import asyncio
from collections.abc import Sequence
from typing import NoReturn
from sqlalchemy import select, delete
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio.session import AsyncSession
from fastapi import HTTPException, status
from sqlalchemy.orm import selectinload
from sqlalchemy.sql.selectable import Select
from core.crud import BaseCrud
from core.deps import AsyncSessionMaker, AsyncSessionMakerDep
from models.courses import Course, Section as SectionModel, Subsection as SubSectionModel
from courses.crud import get_course
from .shemas import CreateSection, CreateSubSection, UpdateSection, UpdateSubSection

from loguru import logger

class SectionCrud(BaseCrud):

    async def create_section(
        self,
        section: CreateSection
    ) -> SectionModel:

        await get_course(self.session, section.course_id)
        section_dict = section.dict()
        subsections = section_dict.pop('subsections', [])
        section_obj = SectionModel(**section_dict)

        if subsections:
            subs = await asyncio.gather(*
                [SubSectionCrud(self.session)
                    .create_subsection(CreateSubSection(**sub)) for sub in subsections]
            )
            section_obj.subsections.extend(subs)

        self.session.add(section_obj)
        await self.session.commit()
        await self.session.refresh(section_obj)
        return section_obj

    async def create_section_task(
        self,
        section: CreateSection,
        sessionmaker: AsyncSessionMakerDep,
    ) -> SectionModel:
        async with sessionmaker() as session:
            section_dict = section.dict()
            subsections = section_dict.pop('subsections', [])
            section_obj = SectionModel(**section_dict)
            session.add(section_obj)
            await session.commit()
            await session.refresh(section_obj)
            await session.merge(section_obj)
            if subsections:
                logger.info("START CREATE SUBS")
                logger.info(subsections)
                subs = await asyncio.gather(*
                    [SubSectionCrud(session)
                        .create_subsection_task(CreateSubSection(**sub, section_id=section_obj.id), sessionmaker) for sub in subsections]
                )
                logger.info("CREATE SUBS")
                logger.info(subs)
                section_obj.subsections.extend(subs)
                logger.info(f"SUBS FOR SECTION : {section_obj.subsections}")
                logger.info("END CREATE SUBS")

            logger.info("OBJECT ADD")
            await session.commit()
            await session.refresh(section_obj)
            logger.info("RETURN")
            return section_obj


    async def delete_section(
        self,
        section_id: int
    ) -> NoReturn:

        section_obj = await self.get_section(section_id, load_selectin=True)
        subssection_ids: list[int] = [s.id for s in section_obj.subsections]
        del_q = (delete(SubSectionModel)
            .where(SubSectionModel.id.in_(subssection_ids)))

        await self.session.execute(del_q)
        await self.session.delete(section_obj)
        await self.session.commit()

    async def patch_section(
        self,
        section_id: int,
        section: UpdateSection
    ) -> SectionModel:
        section_obj = await self.get_section(section_id)
        for key, val in section.dict().items():
            if section.dict().get(key, None):
                setattr(section_obj, key, val)

        await self.session.commit()
        await self.session.refresh(section_obj)

        return section_obj

    @staticmethod
    def get_section_query(section_id: int) -> Select[tuple[SectionModel]]:
        return select(SectionModel).where(SectionModel.id == section_id)

    @staticmethod
    def get_selectin_section_query(section_id: int) -> Select[tuple[SectionModel]]:
        return (select(SectionModel)
            .where(SectionModel.id == section_id)
            .options(selectinload(SectionModel.subsections))
        )

    async def get_section(
        self,
        section_id: int,
        load_selectin: bool = False
    ) -> SectionModel:
        if load_selectin:
            q = self.get_selectin_section_query(section_id)
        else:
            q = self.get_section_query(section_id)

        res = await self.session.execute(q)
        try:
            return res.scalar_one()
        except NoResultFound:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"id": "Раздел не найден!"})


    async def get_list_section(
        self,
        course_id: int
    ) -> Sequence[SectionModel]:
        q = select(SectionModel).where(SectionModel.course_id == course_id)
        res = await self.session.execute(q)
        return res.scalars().all()


class SubSectionCrud(BaseCrud):
    async def create_subsection(
        self,
        subsection: CreateSubSection
    ) -> SubSectionModel:
        section_crud = SectionCrud(self.session)
        await section_crud.get_section(subsection.section_id)
        subsection_obj = SubSectionModel(**subsection.dict())
        self.session.add(subsection_obj)

        await self.session.commit()
        await self.session.refresh(subsection_obj)
        return subsection_obj

    async def create_subsection_task(
        self,
        subsection: CreateSubSection,
        sessionmaker
    ) -> SubSectionModel:
        async with sessionmaker() as session:
            subsection_obj = SubSectionModel(**subsection.dict())
            session.add(subsection_obj)

            await session.commit()
            await session.refresh(subsection_obj)
            return subsection_obj


    async def delete_subsection(
        self,
        subsection_id: int
    ) -> NoReturn:
        # fix this - delete all tasks ?
        subsection_obj = await self.get_subsection(subsection_id)
        await self.session.delete(subsection_obj)
        await self.session.commit()


    async def patch_subsection(
        self,
        subsection_id: int,
        updated_subsection: UpdateSubSection
    ) -> SubSectionModel:
        subsection_obj = await self.get_subsection(subsection_id)
        for key, val in updated_subsection.dict().items():
            if updated_subsection.dict()[key]:
                setattr(subsection_obj, key, val)

        await self.session.commit()
        await self.session.refresh(subsection_obj)
        return subsection_obj


    async def get_subsection(
        self,
        subsection_id: int
    ) -> SubSectionModel:
        q = select(SubSectionModel).where(SubSectionModel.id == subsection_id)
        res = await self.session.execute(q)
        try:
            return res.scalar_one()
        except NoResultFound:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"id": "Подраздел не найден!"})


    async def get_list_subsection(
        self,
        section_id: int
    ) -> Sequence[SubSectionModel]:

        section_crud = SectionCrud(self.session)
        await section_crud.get_section(section_id)
        q = select(SubSectionModel).where(SubSectionModel.section_id == section_id)

        res = await self.session.execute(q)
        return res.scalars().all()
