from pydantic import BaseModel


class Task(BaseModel):
    pass


class CreateTask(BaseModel):
    pass


class UpdateTask(BaseModel):
    pass


class TaskResponse(BaseModel):
    pass
