
from fastapi import status
from fastapi.routing import APIRouter
from starlette.responses import Response

from users.deps import CurActiveUserDep

from . import crud
from categories.shemas import CreateCategory, CategoryResponse, UpdateCategory
from core.deps import SessionDep
from loguru import logger


router = APIRouter(tags=['categories'], prefix='/categories')


@router.post('/create')
async def create(session: SessionDep, category: CreateCategory, current_user: CurActiveUserDep) -> CategoryResponse:
    category_obj = await crud.create_category(session, category)
    return CategoryResponse(**category_obj.to_dict())


@router.patch('/update/{category_id}')
async def update(session: SessionDep,
    category_id: int,
    category: UpdateCategory,
    current_user: CurActiveUserDep
) -> CategoryResponse:
    category_obj = await crud.update_category(session, category_data=category, category_id=category_id)
    return CategoryResponse(**category_obj.to_dict())


@router.delete('/delete/{category_id}')
async def delete(session: SessionDep, category_id: int, current_user: CurActiveUserDep):
    await crud.delete_category(session, category_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get('/get/{category_id}')
async def get(session: SessionDep,
    category_id: int
) -> CategoryResponse:

    category_obj = await crud.get_category(session, category_id)
    return CategoryResponse(**category_obj.to_dict())


@router.get('/list')
async def list(
    session: SessionDep,
) -> list[CategoryResponse]:
    categories = await crud.get_list_categories(session)
    logger.info(categories)
    return [CategoryResponse(**cat.to_dict()) for cat in categories]
