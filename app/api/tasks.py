from fastapi import APIRouter, Depends, Form, File, HTTPException, UploadFile, status

from crud.tasks import TaskCrud
from utils.tasks import TaskUtils
from core.deps import SessionDep
from media_helpers import check_content_type
from deps.tasks import TaskCrudDp
from deps.users import CurActiveUserDep

from shemas.tasks import (
    Answer,
    CreateTask,
    TaskResponse,
    TaskType,
    UpdateTask,
    generate_task_response,
)
from loguru import logger

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post(
    "/create", response_model=TaskResponse, status_code=status.HTTP_201_CREATED
)
async def create_task(
    task_crud: TaskCrudDp,
    current_user: CurActiveUserDep,
    video: UploadFile,
    task_tests: list[UploadFile] = File(None),
    task_for_create: CreateTask = Depends(CreateTask.as_form),
):
    check_content_type(["video/mp4"], video)
    if task_tests:
        [check_content_type(["text/plain", "text/x-python"], f) for f in task_tests]
    obj = await task_crud.create_task(task_for_create, video, task_tests)
    return generate_task_response(obj, task_for_create.task_type.name)


@router.get("/{task_id}", response_model=TaskResponse, status_code=status.HTTP_200_OK)
async def get_task(task_crud: TaskCrudDp, current_user: CurActiveUserDep, task_id: int):
    obj = await task_crud.get_task(task_id)
    task_type = (
        await task_crud.get_task_utils().get_task_type_object(obj.task_type_id),
    )
    return generate_task_response(obj, task_type[0])


@router.delete("/delete/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_crud: TaskCrudDp, current_user: CurActiveUserDep, task_id: int
):
    await task_crud.delete_task(task_id)


@router.patch(
    "/patch/{task_id}", response_model=TaskResponse, status_code=status.HTTP_200_OK
)
async def patch_task(
    task_crud: TaskCrudDp,
    current_user: CurActiveUserDep,
    task_id: int,
    new_task_data: UpdateTask = Depends(UpdateTask.as_form),
    video: UploadFile = File(None),
):
    check_content_type(["video/mp4"], video)
    obj = await task_crud.patch_task(task_id, new_task_data, video)
    task_type = await task_crud.get_task_utils().get_task_type_object(obj.task_type_id)
    return generate_task_response(obj, task_type)


@router.post(
    "/add-answers/{task_id}",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
async def add_answers_for_task(
    session: SessionDep,
    current_user: CurActiveUserDep,
    task_id: int,
    answers: list[Answer],
):
    task_obj = await TaskCrud(session).get_task(task_id)
    task_type = task_obj.task_type.name
    if task_type != "test":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"task_type": "task type is not 'test' !"},
        )
    await TaskUtils(session).create_answers(answers, task_obj)
    return generate_task_response(task_obj, task_type)
