from fastapi import Depends
from typing import Annotated
from core.deps import SessionDep
from crud.submissions import SubmissionCrud


def get_submissions_crud(session: SessionDep) -> SubmissionCrud:
    return SubmissionCrud(session)


SubmissionCrudDp = Annotated[SubmissionCrud, Depends(get_submissions_crud)]
