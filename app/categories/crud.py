from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, func, select, Row
from loguru import logger
from collections.abc import Sequence

from .utils import get_courses_with_single_or_few_categories
from models.categories import Category as CategoryModel, CourseHasCategory
from .shemas import CreateCategory, UpdateCategory

"""
Есть дублирование кода, можно сделать рефакторинг и сделать методы-ресиверы
"""

async def create_category(session: AsyncSession, category: CreateCategory) -> CategoryModel:

    category_obj = CategoryModel(
        title=category.title,
    )
    session.add(category_obj)
    try:
        await session.commit()
        await session.refresh(category_obj)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Категория уже сущесвует")

    return category_obj


async def update_category(
    session: AsyncSession,
    category_data: UpdateCategory,
    category_id: int,
) -> CategoryModel:

    category_obj = await get_category(session, category_id)

    category_dict = category_data.dict(exclude_unset=True)
    for key, val in category_dict.items():
        setattr(category_obj, key, val)

    try:
        await session.commit()
        await session.refresh(category_obj)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Категория уже сущесвует")

    return category_obj


async def delete_category(
    session: AsyncSession,
    category_id: int) -> None:

    category_obj = await get_category(session,category_id)

    async with session.begin_nested():

        empty_courses_ids = await get_courses_with_single_or_few_categories(session, category_id)

        if empty_courses_ids:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="У одного или нескольких курсов это единственная категория!"
            )

        await session.execute(delete(CourseHasCategory)
            .where(CourseHasCategory.category_id == category_id)
        )

        await session.delete(category_obj)
        await session.commit()


async def get_category(
    session: AsyncSession,
    category_id: int
) -> CategoryModel:

    q = select(CategoryModel).where(CategoryModel.id == category_id)
    detail = {"id": "Объект не найден"}

    res = await session.execute(q)
    res = res.scalar_one_or_none()
    if not res:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
    return res


async def get_list_categories(
    session: AsyncSession
) -> Sequence[CategoryModel]:
    res = await session.execute(select(CategoryModel))
    res = res.scalars().all()
    logger.info(res)
    return res
