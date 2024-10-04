import asyncio

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio.session import async_sessionmaker

from models.courses import Course, Section as SectionModel, Subsection as SubSectionModel
from sections.shemas import CreateSection, CreateSubSection
from sections.crud import SectionCrud, SubSectionCrud

from .shemas import CreateCourseStruct
from .crud import CourseCrud

from loguru import logger

class CourseStruct:
    def __init__(self, sessionmaker: async_sessionmaker[AsyncSession]) -> None:
        self.sessionmaker = sessionmaker

    async def __struct_create(self, struct: CreateCourseStruct, course_id: int) -> Course:
        """Create sections and subsections"""
        async with self.sessionmaker() as session:
            course_obj = await CourseCrud(session).get_course(course_id)

            tasks = [asyncio.create_task(self.__create_section_task(
                CreateSection(**s.dict(), course_id=course_id))) for s in struct.sections]

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
        subsections = section_dict.pop('subsections', [])
        async with self.sessionmaker() as session:
            section_crud = SectionCrud(session)
            section_obj = await section_crud.create_section(section)

            tasks = [asyncio.create_task(
                        self.__create_subsection_task(CreateSubSection(**sub, section_id=section_obj.id)))
                    for sub in subsections
                    ]
            section_obj_with_subs = await section_crud.add_subsections_for_section(section_obj, subsections, tasks)
            return section_obj_with_subs


    async def __create_subsection_task(
        self,
        subsection: CreateSubSection,
    ) -> SubSectionModel:
        async with self.sessionmaker() as session:
            return await SubSectionCrud(session).create_subsection(subsection)

    # this method must be return CourseAllData object - valid Pydantic model
    async def get_course_struct(self, struct: CreateCourseStruct, course_id: int) -> Course:
        return await self.__struct_create(struct, course_id)
