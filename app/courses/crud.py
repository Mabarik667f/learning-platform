from fastapi import HTTPException, UploadFile, status
from sqlalchemy import delete, Row
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.sql import select

from core.crud import BaseCrud
from models.categories import Category, CourseHasCategory
from models.courses import Course as CourseModel
from categories.utils import get_list_categories
from collections.abc import Sequence
from media_helpers import UploadMediaFile, delete_dir_media

from .utils import CourseUtils
from .shemas import CourseListQueryParams, CreateCourse, UpdateCourse

from loguru import logger


class CourseCrud(BaseCrud):
    async def create_course(self, course_data: CreateCourse, img: UploadFile) -> CourseModel:
        cr_dict = course_data.dict()
        category_ids = cr_dict.pop("categories")
        cr_dict['img'] = "/"
        course = CourseModel(**cr_dict)

        categories = await get_list_categories(self.session, category_ids=category_ids)
        for category in categories:
            course.categories.append(
                CourseHasCategory(course=course, category=category)
            )

        self.session.add(course)
        await self.session.flush()

        upload_media = UploadMediaFile(course.id, self.session)
        await upload_media.write_img_for_course(course, img)

        await self.session.commit()
        await self.session.refresh(course)
        return course

    async def delete_course(self, course_id: int) -> None:

        course_obj = await self.get_course(course_id)
        q = delete(CourseHasCategory).where(
            CourseHasCategory.course_id == course_obj.id
        )

        async with self.session.begin_nested():
            await self.session.execute(q)
            await self.session.delete(course_obj)
            await self.session.commit()

        delete_dir_media(course_obj.base_media_path_for_course())

    async def patch_course(
        self, course_data: UpdateCourse, course_id: int, img: UploadFile
    ) -> CourseModel:
        course_obj = await self.get_course(course_id)
        for key, val in course_data.dict().items():
            if val is not None:
                setattr(course_obj, key, val)

        if img:
           await self.get_course_utils().upload_course_img(course_obj, img)

        await self.session.commit()
        await self.session.refresh(course_obj)
        return course_obj

    async def get_course(self, course_id: int) -> CourseModel:
        q = select(CourseModel).where(CourseModel.id == course_id)
        res = await self.session.execute(q)
        try:
            res = res.scalar_one()
            return res
        except NoResultFound:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"id": "Курс не найден!"},
            )

    async def get_list_course(
        self, params: CourseListQueryParams, limit: int, offset: int
    ) -> Sequence[CourseModel]:
        q = select(CourseModel)
        if params.min_price is not None:
            q = q.filter(CourseModel.price >= params.min_price)

        if params.max_price is not None:
            q = q.filter(CourseModel.price <= params.max_price)

        if params.difficulties is not None:
            q = q.filter(CourseModel.difficulty.in_(params.difficulties))
        if params.categories:
            q = q.filter(
                CourseModel.id.in_(
                    select(CourseHasCategory.course_id).filter(
                        CourseHasCategory.category_id.in_(params.categories)
                    )
                )
            )
        # add limit + offset
        res = await self.session.execute(q)
        return res.scalars().all()

    def get_course_utils(self):
        return CourseUtils(self.session)
