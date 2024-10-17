import datetime
from fastapi import HTTPException, UploadFile, status
from sqlalchemy import select, delete
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio.session import AsyncSession
from pathlib import Path

from models.courses import (
    Course as CourseModel,
    Section as SectionModel,
    Subsection as SubsectionModel,
    Task as TaskModel,
)
from core.crud import BaseCrud
from .shemas import Answer, CreateTask, TaskTest, TaskType, UpdateTask
from .utils import TaskUtils

from helpers import UploadMediaFile

from loguru import logger


class TaskCrud(BaseCrud):

    def __init__(self, session: AsyncSession) -> None:
        self.utils = TaskUtils(session)
        super().__init__(session)

    async def create_task(
        self,
        task_for_create: CreateTask,
        video: UploadFile,
        task_tests: list[UploadFile] | None = None,
    ) -> TaskModel:
        task_dict = task_for_create.dict()
        answers = [Answer(**ans) for ans in task_dict.pop("answers")]

        task_type_id = await self.utils.get_task_type_id(
            TaskType(name=task_dict.pop("task_type").get("name"))
        )

        task_obj = TaskModel(**task_dict, task_type_id=task_type_id)
        self.session.add(task_obj)

        await self.session.flush()

        upload_media = await self.get_upload_media(task_obj)
        await upload_media.write_video_for_task(task_obj, video)

        await self.utils.create_answers(answers, task_obj)
        if task_tests:
            await self.utils.create_tests_for_question(
                task_obj, task_tests, upload_media
            )
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

    async def patch_task(self, task_id: int, task_for_update: UpdateTask, file: UploadFile) -> TaskModel:
        obj = await self.get_task(task_id)
        task_dict = task_for_update.dict()

        if task_dict.get("task_type"):
            task_type_id = await self.utils.get_task_type_id(
                TaskType(name=task_dict["task_type"]["name"])
            )
            setattr(obj, "task_type_id", task_type_id)

        if file:
            upload_media = await self.get_upload_media(obj)
            await upload_media.write_video_for_task(obj, file)

        for key, val in task_dict.items():
            if task_dict[key] and isinstance(task_dict[key], (str, int)):
                setattr(obj, key, val)

        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    def get_task_utils(self) -> TaskUtils:
        return TaskUtils(self.session)

    async def get_upload_media(self, task_obj: TaskModel) -> UploadMediaFile:
        course_id = await self.utils.get_course_id(task_obj)
        return UploadMediaFile(course_id, self.session)
