from models.courses import Submission as SubmissionModel
from shemas.submissions import NewSubmission
from core.crud import BaseCrud

from loguru import logger


class SubmissionCrud(BaseCrud):

    async def new_submission(self, new_sub: NewSubmission) -> SubmissionModel:
        sub = SubmissionModel(**new_sub.dict())
        self.session.add(sub)
        await self.session.commit()
        await self.session.refresh(sub)
        return sub

    async def get_submission(self, submission_id: int) -> SubmissionModel:
        return await self.session.get_one(SubmissionModel, submission_id)


    async def set_submission_status(self, submission_id: int, todo: bool) -> SubmissionModel:
        sub = await self.session.get_one(SubmissionModel, submission_id)
        sub.todo = todo

        await self.session.commit()
        await self.session.refresh(sub)
        return sub
