from datetime import datetime
from pydantic import BaseModel
from pydantic.fields import Field

class Submission(BaseModel):
    task_id: int = Field(gt=0)
    user_id: int = Field(gt=0)


class NewSubmission(Submission):
    submission_code: str = Field(default="")
    submission_answer: str = Field(default="")


class SubmissionResponse(Submission):
    submission_date: datetime
    submission_code: str = Field(default="")
    submission_answer: str = Field(default="")
    todo: bool = Field(default=False)

    class Config:
        from_attributes = True
