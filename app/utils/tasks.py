from fastapi import UploadFile
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from media_helpers import UploadMediaFile
from core.crud import BaseCrud
from models.courses import (
    TaskType as TaskTypeModel,
    Answer as AnswerModel,
    Task as TaskModel,
    TaskTest as TaskTestModel,
    Course as CourseModel,
    Section as SectionModel,
    Subsection as SubsectionModel,
)
from shemas.tasks import Answer, TaskType, TaskTest
from loguru import logger

class TaskUtils(BaseCrud):

    async def get_task_type_id(self, task_type: TaskType) -> int:
        q = select(TaskTypeModel.id).filter(TaskTypeModel.name == task_type.name)
        res = await self.session.execute(q)
        try:
            return res.scalar_one()
        except NoResultFound:
            raise NoResultFound("Task type not found")

    async def get_task_type_object(self, task_type_id: int) -> str:

        q = select(TaskTypeModel.name).filter(TaskTypeModel.id == task_type_id)
        res = await self.session.execute(q)
        try:
            return res.scalar_one()
        except NoResultFound:
            raise NoResultFound("Task type not found")

    async def create_answers(self, answers: list[Answer], task: TaskModel) -> None:
        for ans in answers:
            ans_obj = AnswerModel(
                text=ans.text.lower(),
                is_correct=ans.is_correct,
                task_id=task.id
            )
            self.session.add(ans_obj)
            task.answers.append(ans_obj)

        await self.session.commit()
        await self.session.refresh(task)

    async def create_tests_for_question(
        self,
        task: TaskModel,
        task_tests: list[UploadFile],
        upload_media: UploadMediaFile,
    ) -> None:
        for file in task_tests:
            test_obj = TaskTestModel(test_file="/", task_id=task.id)
            self.session.add(test_obj)
            await self.session.flush()
            await upload_media.write_test_for_task(test_obj, file)
            task.task_tests.append(test_obj)
        await self.session.commit()
        await self.session.refresh(task)

    async def get_course_id(self, task_obj: TaskModel) -> int:
        q = (
            select(CourseModel.id)
            .join(SectionModel)
            .join(SubsectionModel)
            .filter(SubsectionModel.id == task_obj.subsection_id)
        )
        res = await self.session.execute(q)
        return res.scalar_one()
