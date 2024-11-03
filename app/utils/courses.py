from fastapi import UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from fastapi import HTTPException
from sqlalchemy.orm import selectinload

from models.courses import Course, Difficulty
from models.categories import Category, CourseHasCategory
from media_helpers import UploadMediaFile


from loguru import logger


class CourseUtils:

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add_categories_to_course(
        self, course_id: int, category_ids: list[int]
    ) -> Course:
        course = await self.get_course_selectionload(course_id)
        q = select(Category).where(
            Category.id.in_(category_ids),
            Category.id.not_in(
                select(CourseHasCategory.category_id).where(
                    CourseHasCategory.course_id == course_id
                )
            ),
        )
        categories_q = await self.session.execute(q)
        added_categories = [category[0] for category in categories_q.all()]

        for i in range(len(added_categories)):
            add_cat_to_course = CourseHasCategory(
                category=added_categories[i], course=course
            )
            self.session.add(add_cat_to_course)

        await self.session.commit()
        await self.session.refresh(course)

        return course

    async def del_category(self, course_id: int, category_id: int) -> Course:
        course = await self.get_course_selectionload(course_id)
        if len(course.categories) > 1:
            q = delete(CourseHasCategory).where(
                CourseHasCategory.course_id == course_id,
                CourseHasCategory.category_id == category_id,
            )

            await self.session.execute(q)
            await self.session.commit()
            await self.session.refresh(course)

            return course
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"course": "У курса должна быть хотя бы 1 категория"},
        )

    async def get_all_difficulties(self) -> list[Difficulty]:
        return [df for df in Difficulty]

    async def get_course_selectionload(self, course_id: int) -> Course:
        course = await self.session.get(
            Course, course_id, options=[selectinload(Course.categories)]
        )
        if course is not None:
            return course

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"course": "Курс не найден !"},
        )

    async def upload_course_img(self, course: Course, img: UploadFile):
        await self.session.flush()
        upload_media = UploadMediaFile(course.id, self.session)
        await upload_media.write_img_for_course(course, img)
