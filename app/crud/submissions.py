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
