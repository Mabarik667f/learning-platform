from typing import Annotated
from fastapi import Depends, Query
from core.deps import SessionDep
from models.courses import Difficulty
from .crud import CourseCrud
from .shemas import CourseListQueryParams


async def get_list_query_params(
    difficulties: list[Difficulty] | None = Query(None),
    min_price: int | None = Query(None),
    max_price: int | None = Query(None),
    categories: list[int] = Query(None),
) -> CourseListQueryParams:
    return CourseListQueryParams(
        difficulties=difficulties,
        min_price=min_price,
        max_price=max_price,
        categories=categories,
    )


async def get_course_crud(session: SessionDep) -> CourseCrud:
    return CourseCrud(session)


ListQueryParamsDp = Annotated[CourseListQueryParams, Depends(get_list_query_params)]
CourseCrudDep = Annotated[CourseCrud, Depends(get_course_crud)]
