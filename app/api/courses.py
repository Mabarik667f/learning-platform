from fastapi import Depends, File, Query, UploadFile, status
from fastapi.responses import Response
from fastapi.routing import APIRouter

from media_helpers import check_content_type
from utils.categories import get_categories_by_ids
from shemas.categories import Category

from deps.users import CurActiveUserDep
from deps.courses import ListQueryParamsDp, CourseCrudDep
from core.deps import AsyncSessionMakerDep, SessionDep
from shemas.courses import (
    AddCategoriesToCourse,
    CourseAllData,
    CourseDifficulty,
    CourseResponse,
    CourseWithCategories,
    CreateCourse,
    CreateCourseStruct,
    UpdateCourse,
)
from services.course_struct import CourseStruct
from utils.courses import CourseUtils

from loguru import logger

router = APIRouter(tags=["courses"], prefix="/courses")


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create(
    course_crud: CourseCrudDep,
    # current_user: CurActiveUserDep,
    img: UploadFile,
    course: CreateCourse = Depends(CreateCourse.as_form),
) -> CourseResponse:
    check_content_type(["image/jpeg", "image/jpg", "image/png"], img)
    course_obj = await course_crud.create_course(course, img)
    return CourseResponse(**course_obj.to_dict())


@router.patch("/patch/{course_id}")
async def patch(
    course_crud: CourseCrudDep,
    current_user: CurActiveUserDep,
    course_id: int,
    course: UpdateCourse = Depends(UpdateCourse.as_form),
    img: UploadFile = File(None),
) -> CourseResponse:
    check_content_type(["image/jpeg", "image/jpg", "image/png"], img)
    course_obj = await course_crud.patch_course(course, course_id, img)
    return CourseResponse(**course_obj.to_dict())


@router.delete("/delete/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(
    course_crud: CourseCrudDep, current_user: CurActiveUserDep, course_id: int
):
    await course_crud.delete_course(course_id)


@router.get("/list")
async def get_list(
    course_crud: CourseCrudDep,
    *,
    params: ListQueryParamsDp,
    limit: int = Query(10),
    offset: int = Query(0)
) -> list[CourseResponse]:
    courses = await course_crud.get_list_course(params, limit, offset)
    return [CourseResponse(**course.to_dict()) for course in courses]


@router.get("/all-difficulties")
async def get_difficulties(session: SessionDep) -> list[CourseDifficulty]:
    difficulties = await CourseUtils(session).get_all_difficulties()
    return [CourseDifficulty(title=df.title()) for df in difficulties]


@router.get("/{course_id}")
async def get(course_crud: CourseCrudDep, course_id: int) -> CourseResponse:
    course = await course_crud.get_course(course_id)
    return CourseResponse(**course.to_dict())


@router.delete("/delete-category/{course_id}/{category_id}")
async def delete_category(
    session: SessionDep,
    current_user: CurActiveUserDep,
    course_id: int,
    category_id: int,
) -> CourseWithCategories:
    course = await CourseUtils(session).del_category(course_id, category_id)
    categories_row = await get_categories_by_ids(session, course.categories)

    categories = [Category(**category.to_dict()) for category in categories_row]
    return CourseWithCategories(**course.to_dict(), categories=categories)


@router.patch("/add-categories/{course-id}")
async def add_categories(
    session: SessionDep,
    current_user: CurActiveUserDep,
    course_id: int,
    added_categories: AddCategoriesToCourse,
) -> CourseWithCategories:
    course = await CourseUtils(session).add_categories_to_course(
        course_id, category_ids=added_categories.category_ids
    )
    categories_row = await get_categories_by_ids(session, course.categories)

    categories = [Category(**category.to_dict()) for category in categories_row]
    return CourseWithCategories(**course.to_dict(), categories=categories)


@router.post(
    "/struct/{course_id}",
    status_code=status.HTTP_201_CREATED,
    response_model=CourseAllData,
)
async def create_course_struct(
    session: SessionDep,
    sessionmaker: AsyncSessionMakerDep,
    # current_user: CurActiveUserDep,
    course_id: int,
    struct: CreateCourseStruct,
):
    return await CourseStruct(sessionmaker).get_course_struct(struct, course_id)
