from fastapi import HTTPException, status
from sqlalchemy import delete, Row
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.sql import select

from models.categories import Category, CourseHasCategory
from models.courses import Course as CourseModel
from categories.utils import get_list_categories
from collections.abc import Sequence

from .shemas import CourseListQueryParams, CreateCourse, UpdateCourse

from loguru import logger


async def create_course(session: AsyncSession, course_data: CreateCourse) -> CourseModel:
    cr_dict = course_data.dict()
    category_ids = cr_dict.pop('categories')
    course = CourseModel(**cr_dict)

    categories = await get_list_categories(session, category_ids=category_ids)
    for category in categories:
        course.categories.append(CourseHasCategory(course=course, category=category))

    session.add(course)
    await session.commit()
    await session.refresh(course)
    return course


async def delete_course(session: AsyncSession, course_id: int) -> None:

    course_obj = await get_course(session, course_id)

    q = delete(CourseHasCategory).where(
            CourseHasCategory.course_id == course_obj.id
        )

    async with session.begin_nested():
        await session.execute(q)
        await session.delete(course_obj)
        await session.commit()


async def patch_course(session: AsyncSession, course_data: UpdateCourse, course_id: int) -> CourseModel:
    course_obj = await get_course(session, course_id)
    for key, val in course_data.dict().items():
        setattr(course_obj, key, val)

    await session.commit()
    await session.refresh(course_obj)
    return course_obj


async def get_course(session: AsyncSession, course_id: int) -> CourseModel:
    q = select(CourseModel).where(CourseModel.id == course_id)
    res = await session.execute(q)
    try:
        res = res.scalar_one()
        return res
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"id": "Курс не найден!"})


async def get_course_selectionload(session: AsyncSession, course_id: int) -> CourseModel:
    course = await session.get(CourseModel, course_id, options=[selectinload(CourseModel.categories)])
    if course is not None:
        return course

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"course": "Курс не найден !"})


async def get_list_course(
    session: AsyncSession,
    params: CourseListQueryParams,
    limit: int,
    offset: int
) -> Sequence[CourseModel]:
    q = select(CourseModel)
    if params.min_price is not None:
        q = q.filter(CourseModel.price >= params.min_price)

    if params.max_price is not None:
        q = q.filter(CourseModel.price <= params.max_price)

    if params.difficulties is not None:
        q = q.filter(CourseModel.difficulty.in_(params.difficulties))
    if params.categories:
        q = q.filter(CourseModel.id.in_(
            select(CourseHasCategory.course_id)
            .filter(CourseHasCategory.category_id.in_(params.categories))
        ))
    # add limit + offset
    res = await session.execute(q)
    return res.scalars().all()
