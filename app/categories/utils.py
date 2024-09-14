from collections.abc import Iterable, Sequence
from loguru import logger
from fastapi import status, HTTPException
from sqlalchemy import Row
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select, func
from models.categories import Category, CourseHasCategory


async def get_list_categories(session: AsyncSession, category_ids: Iterable[list[int]]) -> Sequence[Category]:
    q = select(Category).where(Category.id.in_(category_ids))
    res = await session.execute(q)
    res = res.scalars().all()
    if not res:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"categories": "not found!"})
    return res


async def get_courses_with_single_or_few_categories(session: AsyncSession, category_id: int) -> list[int]:
    query = (
        select(CourseHasCategory.course_id)
        .where(CourseHasCategory.category_id == category_id,
            CourseHasCategory.course_id.in_(
                select(CourseHasCategory.course_id)
                .group_by(CourseHasCategory.course_id)
                .having(func.count(CourseHasCategory.category_id) <= 1))
        )
    )


    result = await session.execute(query)
    empty_courses_ids = result.scalars().all()
    return list(empty_courses_ids)


async def get_categories_by_ids(
    session: AsyncSession,
    course_has_category: list[CourseHasCategory]
)-> Sequence[Category]:
    q = (select(Category)
        .where(Category.id.in_(c.category_id for c in course_has_category)))
    res = await session.execute(q)
    return res.scalars().all()
