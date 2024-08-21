from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, select
from loguru import logger

from categories.models import Category as CategoryModel

from .shemas import CreateCategory, UpdateCategory

"""
Есть дублирование кода, можно сделать рефакторинг и сделать методы-ресиверы
"""

async def create_category(session: AsyncSession, category: CreateCategory) -> CategoryModel:

    category_obj = CategoryModel(
        title=category.title,
        slug=category.slug
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
    category_id: int | None=None,
    category_slug: str | None=None) -> CategoryModel:

    category_obj = await get_category(session,
        category_id=category_id,
        category_slug=category_slug)

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
    category_id: int | None=None,
    category_slug: str | None=None) -> None:

    category_obj = await get_category(session,
        category_slug=category_slug,
        category_id=category_id)

    if category_id:
        q = delete(CategoryModel).where(CategoryModel.id == category_id)
    else:
        q = delete(CategoryModel).where(CategoryModel.slug == category_slug)

    await session.execute(q)
    await session.commit()


async def get_category(
    session: AsyncSession,
    category_id: int | None=None,
    category_slug: str | None=None) -> CategoryModel:

    if category_id:
        q = select(CategoryModel).where(CategoryModel.id == category_id)
        detail = {"id": "Объект не найден"}
    elif category_slug:
        q = select(CategoryModel).where(CategoryModel.slug == category_slug)
        detail = {"slug": "Объект не найден"}
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="no params for by get method")

    res = await session.execute(q)
    res = res.scalar_one_or_none()
    if not res:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
    return res
