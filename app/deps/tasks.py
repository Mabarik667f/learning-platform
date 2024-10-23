from fastapi import Depends
from typing import Annotated
from core.deps import SessionDep
from crud.tasks import TaskCrud


def get_task_crud(session: SessionDep) -> TaskCrud:
    return TaskCrud(session)


TaskCrudDp = Annotated[TaskCrud, Depends(get_task_crud)]
