from collections.abc import Container
from fastapi import HTTPException, status
from sqlalchemy import select, delete
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio.session import AsyncSession

from models.courses import Task as TaskModel
from core.crud import BaseCrud
from .shemas import Answer, CreateTask, TaskTest, TaskType, UpdateTask
from .utils import TaskUtils

from loguru import logger


class TaskCrud(BaseCrud):

    def __init__(self, session: AsyncSession) -> None:
        self.utils = TaskUtils(session)
        super().__init__(session)

    async def create_task(self, task_for_create: CreateTask) -> TaskModel:
        task_dict = task_for_create.dict()
        answers = [Answer(**ans) for ans in task_dict.pop("answers")]
        task_tests = [TaskTest(**t) for t in task_dict.pop("task_tests")]

        task_type_id = await self.utils.get_task_type_id(
            TaskType(name=task_dict.pop("task_type").get("name"))
        )

        if task_dict.get("video_path") is not None:
            task_dict["video_path"] = str(task_dict.get("video_path"))

        task_obj = TaskModel(**task_dict, task_type_id=task_type_id)
        self.session.add(task_obj)

        await self.utils.create_answers(answers, task_obj)
        await self.utils.create_tests_for_question(task_tests, task_obj)

        await self.session.commit()
        await self.session.refresh(task_obj)
        return task_obj

    async def get_task(self, task_id: int) -> TaskModel:
        q = select(TaskModel).filter(TaskModel.id == task_id)
        try:
            res = await self.session.execute(q)
            return res.scalar_one()
        except NoResultFound:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"task": "Задание не найдено !"},
            )

    async def delete_task(self, task_id: int) -> None:
        obj = await self.get_task(task_id)
        await self.session.delete(obj)
        await self.session.commit()

    async def patch_task(self, task_id: int, task_for_update: UpdateTask) -> TaskModel:
        obj = await self.get_task(task_id)
        task_dict = task_for_update.dict()
        task_dict["video_path"] = str(task_dict.get("video_path"))

        if task_dict.get('task_type'):
            task_type_id = await self.utils.get_task_type_id(TaskType(name=task_dict['task_type']['name']))
            setattr(obj, "task_type_id", task_type_id)

        for key, val in task_dict.items():
            logger.info(task_dict[key])
            if task_dict[key] and isinstance(task_dict[key], (str, int)):
                logger.info(task_dict[key])
                setattr(obj, key, val)

        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    def get_task_utils(self) -> TaskUtils:
        return TaskUtils(self.session)
