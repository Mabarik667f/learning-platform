from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio.session import AsyncSession

from models.courses import Task as TaskModel

from .shemas import CreateTask


async def create_task(session: AsyncSession, task_for_create: CreateTask) -> TaskModel:
    task_dict = task_for_create.dict()
