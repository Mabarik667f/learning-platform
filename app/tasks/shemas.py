from pydantic import BaseModel, Field, FilePath
from models.courses import (
    Answer as AnswerModel,
    TaskTest as TaskTestModel,
    Task as TaskModel
)


class Task(BaseModel):
    text: str = Field(default="")
    video_path: FilePath | None = Field(default=None)
    scores: int = Field(default=1, gt=0)


class CreateTask(Task):
    task_type: "TaskType"
    subsection_id: int = Field(gt=0)
    answers: list["Answer"] = Field(default=[])
    task_tests: list["TaskTest"] = Field(default=[])


class UpdateTask(Task):
    task_type: "TaskType"


class AddTaskContent:
    answers: list["Answer"] = Field(default=[])
    task_tests: list["TaskTest"] = Field(default=[])


class TaskResponse(Task):
    id: int
    subsection_id: int
    task_type: "TaskType"
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
    test_file: FilePath


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
