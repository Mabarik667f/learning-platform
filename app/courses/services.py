import asyncio

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio.session import async_sessionmaker
from sqlalchemy.orm import joinedload

from app.categories.shemas import CategoryResponse
from models.courses import (
    Course,
    Section as SectionModel,
    Subsection as SubSectionModel,
)
from sections.shemas import (
    CreateSection,
    CreateSubSection,
    SectionWithSubsectionsResponse,
    SubSectionResponse,
)
from sections.crud import SectionCrud, SubSectionCrud

from categories.utils import get_categories_by_ids
from .shemas import CreateCourseStruct, CourseAllData, Category
from .crud import CourseCrud

from loguru import logger


class CourseStruct:
    def __init__(self, sessionmaker: async_sessionmaker[AsyncSession]) -> None:
        self.sessionmaker = sessionmaker

    async def __struct_create(
        self, struct: CreateCourseStruct, course_id: int
    ) -> Course:
        """Create sections and subsections"""
        async with self.sessionmaker() as session:
            res = await session.execute(
                select(Course)
                .options(joinedload(Course.categories))
                .where(Course.id == course_id)
            )
            course_obj = res.unique().scalar_one()

            tasks = [
                asyncio.create_task(
                    self.__create_section_task(
                        CreateSection(**s.dict(), course_id=course_id)
                    )
                )
                for s in struct.sections
            ]

            for coro in asyncio.as_completed(tasks):
                section = await coro
                course_obj.sections.append(section)

            await session.refresh(course_obj)
            await session.commit()
            return course_obj

    async def __create_section_task(
        self,
        section: CreateSection,
    ) -> SectionModel:

        section_dict = section.dict()
        subsections = section_dict.pop("subsections", [])
        async with self.sessionmaker() as session:
            section_crud = SectionCrud(session)
            section_obj = await section_crud.create_section(section)

            tasks = [
                asyncio.create_task(
                    self.__create_subsection_task(
                        CreateSubSection(**sub, section_id=section_obj.id)
                    )
                )
                for sub in subsections
            ]
            section_obj_with_subs = await section_crud.add_subsections_for_section(
                section_obj, subsections, tasks
            )
            return section_obj_with_subs

    async def __create_subsection_task(
        self,
        subsection: CreateSubSection,
    ) -> SubSectionModel:
        async with self.sessionmaker() as session:
            return await SubSectionCrud(session).create_subsection(subsection)

    async def get_course_struct(
        self, struct: CreateCourseStruct, course_id: int
    ) -> CourseAllData:
        obj = await self.__struct_create(struct, course_id)
        async with self.sessionmaker() as session:
            categories = await get_categories_by_ids(session, obj.categories)

        cats = [CategoryResponse(**cat.to_dict()) for cat in categories]
        sections = []
        for section in obj.sections:
            subs = [SubSectionResponse(**sub.to_dict()) for sub in section.subsections]
            sections.append(
                SectionWithSubsectionsResponse(**section.to_dict(), subsections=subs)
            )

        return CourseAllData(**obj.to_dict(), categories=cats, sections=sections)
