from fastapi import APIRouter, status

from users.deps import CurActiveUserDep

from .shemas import (
    CreateTask,
    TaskResponse,
    UpdateTask,
    generate_task_response,
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
    return generate_task_response(obj, task_for_create.task_type.name)


@router.get("/{task_id}", response_model=TaskResponse, status_code=status.HTTP_200_OK)
async def get_task(task_crud: TaskCrudDp, current_user: CurActiveUserDep, task_id: int):
    obj = await task_crud.get_task(task_id)
    task_type = (
        await task_crud.get_task_utils().get_task_type_object(obj.task_type_id),
    )
    return generate_task_response(obj, task_type[0])


@router.delete("/delete/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_crud: TaskCrudDp, current_user: CurActiveUserDep, task_id: int):
    await task_crud.delete_task(task_id)


@router.patch("/patch/{task_id}", response_model=TaskResponse, status_code=status.HTTP_200_OK)
async def patch_task(
    task_crud: TaskCrudDp,
    current_use: CurActiveUserDep,
    task_id: int,
    new_task_data: UpdateTask
):
    obj = await task_crud.patch_task(task_id, new_task_data)
    task_type = (
        await task_crud.get_task_utils().get_task_type_object(obj.task_type_id)
    )
    return generate_task_response(obj, task_type)
