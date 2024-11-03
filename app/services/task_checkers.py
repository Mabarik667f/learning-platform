from abc import ABC, abstractmethod

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from models.courses import Answer, Submission
from exc import UnSupportedSubmissionException


class SubmissionChecker(ABC):

    def __init__(self, session: AsyncSession, submission: Submission) -> None:
        self.session = session
        self.submission = submission

    async def check(self) -> bool:
        sub_type = self.submission.task.task_type.name
        args = [self.session, self.submission]
        match sub_type:
            case "test":
                return await TestSubmissionChecker(*args).check()
            case "code":
                return await CodeSubmissionChecker(*args).check()
            case _:
                raise UnSupportedSubmissionException("Unsupported type of submission!")


class TestSubmissionChecker(SubmissionChecker):

    async def check(self) -> bool:
        q = select(Answer.is_correct).filter(
            Answer.text == self.submission.submission_answer.lower()
        )
        try:
            res = await self.session.execute(q)
            return res.scalar_one()
        except NoResultFound:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="answer not found"
            )


class CodeSubmissionChecker(SubmissionChecker):

    async def check(self) -> bool:
        pass
