from fastapi import APIRouter, status

from users.deps import CurActiveUserDep

from .shemas import (
    CreateTask,
    TaskResponse,
    TaskType,
    from_obj_to_model_answers,
    from_obj_to_model_tests,
)
from .deps import TaskCrudDp

from loguru import logger

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post(
    "/create", response_model=TaskResponse, status_code=status.HTTP_201_CREATED
)
async def create_task(
    task_crud: TaskCrudDp,
    current_user: CurActiveUserDep,
    task_for_create: CreateTask,
):
    obj = await task_crud.create_task(task_for_create)
    return TaskResponse(
        **obj.to_dict(),
        task_type=task_for_create.task_type,
        answers=from_obj_to_model_answers(obj.answers),
        task_tests=from_obj_to_model_tests(obj.task_tests)
    )


@router.get("/{task_id}", response_model=TaskResponse, status_code=status.HTTP_200_OK)
async def get_task(task_crud: TaskCrudDp, current_user: CurActiveUserDep, task_id: int):
    obj = await task_crud.get_task(task_id)
    task_type = (
        await task_crud.get_task_utils().get_task_type_object(obj.task_type_id),
    )
    return TaskResponse(
        **obj.to_dict(),
        task_type=TaskType(name=task_type[0]),
        answers=from_obj_to_model_answers(obj.answers),
        task_tests=from_obj_to_model_tests(obj.task_tests)
    )
