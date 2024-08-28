from fastapi import Query, status
from fastapi.responses import Response
from fastapi.routing import APIRouter

from categories.utils import get_categories_by_ids
from categories.shemas import Category
from users.deps import CurActiveUserDep
from core.deps import SessionDep
from .shemas import (AddCategoriesToCourse, CourseAllData,
    CourseListQueryParams, CourseResponse, CourseWithCategories,
    CreateCourse, UpdateCourse)
from .deps import ListQueryParamsDp
from .utils import add_categories_to_course, del_category
from . import crud

from loguru import logger

router = APIRouter(tags=['courses'], prefix='/courses')


@router.post('/create', status_code=status.HTTP_201_CREATED)
async def create(
    session: SessionDep,
    current_user: CurActiveUserDep,
    course: CreateCourse
) -> CourseResponse:
    course_obj = await crud.create_course(session, course)
    return CourseResponse(**course_obj.to_dict())


@router.patch("/patch-data")
async def patch(
    session: SessionDep,
    current_user: CurActiveUserDep,
    course_id: int,
    course: UpdateCourse
) -> CourseResponse:
    course_obj = await crud.patch_course(session, course, course_id)
    return CourseResponse(**course_obj.to_dict())


@router.delete('/delete')
async def delete(
    session: SessionDep,
    current_user: CurActiveUserDep,
    course_id: int
) -> Response:
    await crud.delete_course(session, course_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# @router.get('/all-data/{course_id}')
# async def get_all_data(
#     session: SessionDep,
#     course_id: int
# ) -> CourseAllData:
#     course = await crud.get_course(session, course_id)
#     return CourseAllData(**course.to_dict())


@router.get("/list")
async def get_list(
    session: SessionDep,
    *,
    params: CourseListQueryParams = ListQueryParamsDp
) -> list[CourseResponse]:
    courses = await crud.get_list_course(session, params)
    return [CourseResponse(**course[0].to_dict()) for course in courses]


@router.get('/{course_id}')
async def get(
    session: SessionDep,
    course_id: int
) -> CourseResponse:
    course = await crud.get_course(session, course_id)
    return CourseResponse(**course.to_dict())


@router.delete('/delete-category/{course_id}/{category_id}')
async def delete_category(
    session: SessionDep,
    current_user: CurActiveUserDep,
    course_id: int,
    category_id: int
) -> CourseWithCategories:
    course = await del_category(session, course_id, category_id)
    categories_row = await get_categories_by_ids(session, course.categories)

    categories = [Category(**category[0].to_dict()) for category in categories_row]
    return CourseWithCategories(**course.to_dict(), categories=categories)


@router.patch('/add-categories/{course-id}')
async def add_categories(
    session: SessionDep,
    current_user: CurActiveUserDep,
    course_id: int,
    added_categories: AddCategoriesToCourse
):
    course = await add_categories_to_course(session, course_id, category_ids=added_categories.category_ids)
    categories_row = await get_categories_by_ids(session, course.categories)

    categories = [Category(**category[0].to_dict()) for category in categories_row]
    return CourseWithCategories(**course.to_dict(), categories=categories)
