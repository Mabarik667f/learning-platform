from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from core.crud import BaseCrud
from models.courses import (
    TaskType as TaskTypeModel,
    Answer as AnswerModel,
    Task as TaskModel,
    TaskTest as TaskTestModel,
)
from .shemas import Answer, TaskType, TaskTest


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
            ans_obj = AnswerModel(**ans.dict(), task_id=task.id)
            self.session.add(ans_obj)
            task.answers.append(ans_obj)

        await self.session.commit()
        await self.session.refresh(task)

    async def create_tests_for_question(
        self, tests: list[TaskTest], task: TaskModel
    ) -> None:
        for test in tests:
            test_obj = TaskTestModel(test_file=str(test.test_file), task_id=task.id)
            self.session.add(test_obj)
            task.task_tests.append(test_obj)
        await self.session.commit()
        await self.session.refresh(task)
