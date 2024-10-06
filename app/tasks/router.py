from fastapi import APIRouter, status

from core.deps import SessionDep
from users.deps import CurActiveUserDep

from .shemas import CreateTask, TaskResponse
from . import crud

router = APIRouter(prefix="tasks", tags=["tasks"])


@router.post("create", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    session: SessionDep, current_user: CurActiveUserDep, task_for_create: CreateTask
):
    obj = await crud.create_task(session, task_for_create)
    return TaskResponse(**obj.to_dict())
