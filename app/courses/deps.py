from fastapi import Depends, Query
from models.courses import Difficulty
from .shemas import CourseListQueryParams


async def get_list_query_params(
    difficulties: list[Difficulty] | None = Query(None),
    min_price: int | None = Query(None),
    max_price: int | None = Query(None),
    categories: list[int] = Query(None)
) -> CourseListQueryParams:
    return CourseListQueryParams(
        difficulties=difficulties,
        min_price=min_price,
        max_price=max_price,
        categories=categories
    )

ListQueryParamsDp = Depends(get_list_query_params)
