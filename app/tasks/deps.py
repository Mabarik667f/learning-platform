from typing import Annotated

from fastapi.params import Depends

from core.deps import SessionDep
from .crud import TaskCrud


def get_task_crud(session: SessionDep) -> TaskCrud:
    return TaskCrud(session)


TaskCrudDp = Annotated[TaskCrud, Depends(get_task_crud)]
