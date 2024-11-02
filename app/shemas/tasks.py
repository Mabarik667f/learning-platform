import json
from typing import Literal
from fastapi import Form
from pydantic import BaseModel, Field, FilePath

from loguru import logger

from models.courses import (
    Answer as AnswerModel,
    TaskTest as TaskTestModel,
    Task as TaskModel,
)


class Task(BaseModel):
    text: str = Field(default="")
    video_path: FilePath | None = Field(default=None)
    scores: int = Field(default=1, gt=0)
    task_type: "TaskType"

class CreateTask(Task):
    subsection_id: int = Field(gt=0)

    @classmethod
    def as_form(
        cls,
        text: str = Form(...),
        scores: int = Form(1),
        subsection_id: int = Form(1),
        task_type: Literal["test", "code", "video"] = Form(),
    ):
        return cls(
            text=text,
            video_path=None,
            scores=scores,
            task_type=TaskType(name=task_type),
            subsection_id=subsection_id,
        )


class UpdateTask(Task):
    pass

    @classmethod
    def as_form(
        cls,
        text: str = Form(...),
        scores: int = Form(1),
        task_type: str = Form(),
    ):
        return cls(
            text=text,
            scores=scores,
            task_type=TaskType(name=json.loads(task_type)["name"]))


class AddTaskContent:
    answers: list["Answer"] = Field(default=[])
    task_tests: list["TaskTest"] = Field(default=[])


class TaskResponse(Task):
    id: int
    subsection_id: int
    answers: list["AnswerResponse"] = Field(default=[])
    task_tests: list["TaskTestResponse"] = Field(default=[])

    class Config:
        from_attributes = True


class TaskType(BaseModel):
    name: str = Field(description="Всегда есть: \n(test, code, video)")


class Answer(BaseModel):
    text: str
    is_correct: bool = Field(default=False)


class AnswerCreate(Answer):
    pass


class AnswerResponse(Answer):
    id: int
    task_id: int = Field(gt=0)

    class Config:
        from_attributes = True


class TaskTest(BaseModel):
    test_file: FilePath | None = None


class CreateTaskTest(TaskTest):
    pass


class UpdateTaskTest(TaskTest):
    pass


class TaskTestResponse(TaskTest):
    id: int
    task_id: int

    class Config:
        from_attributes = True


def from_obj_to_model_answers(answers: list[AnswerModel]) -> list[AnswerResponse]:
    return [AnswerResponse(**ans.to_dict()) for ans in answers]


def from_obj_to_model_tests(tests: list[TaskTestModel]) -> list[TaskTestResponse]:
    return [TaskTestResponse(**t.to_dict()) for t in tests]


def generate_task_response(obj: TaskModel, task_type: str) -> TaskResponse:
    return TaskResponse(
        **obj.to_dict(),
        task_type=TaskType(name=task_type),
        answers=from_obj_to_model_answers(obj.answers),
        task_tests=from_obj_to_model_tests(obj.task_tests)
    )
