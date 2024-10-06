from pydantic import BaseModel, Field


class Task(BaseModel):
    text: str = Field(default="")
    video_path: str = Field(default="/")
    todo: bool = Field(default=False, description="Выполнено")
    scores: int = Field(default=1, gt=0)


class CreateTask(Task):
    task_type: "TaskType"
    subsection_id: int = Field(default=1)
    answers: list["Answer"] = Field(default=[])
    task_tests: list["TaskTest"] = Field(default=[])


class UpdateTask(Task):
    pass


class AddTaskContent:
    answers: list["Answer"] = Field(default=[])
    task_tests: list["TaskTest"] = Field(default=[])


class TaskResponse(Task):
    id: int
    subsection_id: int
    task_type: "TaskType"
    answers: list["Answer"] = Field(default=[])
    task_tests: list["TaskTest"] = Field(default=[])

    class Config:
        from_attributes = True


class TaskType(BaseModel):
    name: str = Field(description="Всегда есть: \n(test, code, video)")


class Answer(BaseModel):
    pass


class TaskTest(BaseModel):
    pass
