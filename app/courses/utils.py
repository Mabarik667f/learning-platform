from fastapi import status
from collections.abc import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Row, delete
from sqlalchemy.orm import selectinload
from fastapi import HTTPException

from . import crud
from .models import Course, Difficulty
from categories.models import Category, CourseHasCategory
from loguru import logger


async def add_categories_to_course(session: AsyncSession, course_id: int, category_ids: list[int]) -> Course:
    course = await crud.get_course_selectionload(session, course_id)
    q = (select(Category)
        .where(Category.id.in_(category_ids),
            Category.id.not_in(
                select(CourseHasCategory.category_id)
                .where(CourseHasCategory.course_id == course_id)
            ))
    )
    categories_q = await session.execute(q)
    added_categories = [category[0] for category in categories_q.all()]

    for i in range(len(added_categories)):
        add_cat_to_course = CourseHasCategory(category=added_categories[i], course=course)
        session.add(add_cat_to_course)

    await session.commit()
    await session.refresh(course)

    return course


async def del_category(session: AsyncSession, course_id: int, category_id: int) -> Course:
    course = await crud.get_course_selectionload(session, course_id)
    if len(course.categories) > 1:
        q = delete(CourseHasCategory).where(
                   CourseHasCategory.course_id == course_id,
                   CourseHasCategory.category_id == category_id
               )

        await session.execute(q)
        await session.commit()
        await session.refresh(course)

        return course
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
        detail={"course": "У курса должна быть хотя бы 1 категория"})



async def get_all_difficulties(session: AsyncSession) -> list[Difficulty]:
    return [df for df in Difficulty]
