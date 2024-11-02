from fastapi import Depends
from typing import Annotated
from utils.tasks import TaskUtils
from core.deps import SessionDep
from crud.tasks import TaskCrud


def get_task_crud(session: SessionDep) -> TaskCrud:
    return TaskCrud(session)

def get_task_utils(session: SessionDep) -> TaskUtils:
    return TaskUtils(session)

TaskCrudDp = Annotated[TaskCrud, Depends(get_task_crud)]
TaskUtilsDp = Annotated[TaskUtils, Depends(get_task_utils)]
