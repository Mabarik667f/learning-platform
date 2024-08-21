
from fastapi import status
from fastapi.routing import APIRouter
from starlette.responses import Response

from users.deps import CurActiveUserDep

from . import crud
from categories.shemas import CreateCategory, CategoryResponse, UpdateCategory
from core.deps import SessionDep
from loguru import logger


router_id = APIRouter(tags=['categories-id'], prefix='/categories/id')
router_slug = APIRouter(tags=['categories-slug'], prefix="/categories/slug")


@router_id.post('/create')
async def create(session: SessionDep, category: CreateCategory, current_user: CurActiveUserDep) -> CategoryResponse:
    category_obj = await crud.create_category(session, category)
    return CategoryResponse(**category_obj.to_dict())


@router_id.patch('/update/{category_id}')
async def update_by_id(session: SessionDep,
    category_id: int,
    category: UpdateCategory,
    current_user: CurActiveUserDep
) -> CategoryResponse:
    category_obj = await crud.update_category(session, category_data=category, category_id=category_id)
    return CategoryResponse(**category_obj.to_dict())


@router_id.delete('/delete/{category_id}')
async def delete_by_id(session: SessionDep, category_id: int, current_user: CurActiveUserDep):
    await crud.delete_category(session, category_id=category_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router_id.get('/get/{category_id}')
async def get_by_id(session: SessionDep,
    current_user: CurActiveUserDep,
    category_id: int
) -> CategoryResponse:

    category_obj = await crud.get_category(session, category_id=category_id)
    return CategoryResponse(**category_obj.to_dict())


@router_slug.patch('/update/{category_slug}')
async def update_by_slug(session: SessionDep,
    category_slug: str,
    category: UpdateCategory,
    current_user: CurActiveUserDep
) -> CategoryResponse:
    category_obj = await crud.update_category(session, category_data=category, category_slug=category_slug)
    return CategoryResponse(**category_obj.to_dict())


@router_slug.delete('/delete/{category_slug}')
async def delete_by_slug(session: SessionDep, category_slug: str, current_user: CurActiveUserDep):
    await crud.delete_category(session, category_slug=category_slug)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router_slug.get('/get/{category_slug}')
async def get_by_slug(session: SessionDep, category_slug: str, current_user: CurActiveUserDep) -> CategoryResponse:
    category_obj = await crud.get_category(session, category_slug=category_slug)
    return CategoryResponse(**category_obj.to_dict())
