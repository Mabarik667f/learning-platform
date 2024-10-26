from fastapi import APIRouter, status
from core.deps import SessionDep
from shemas.submissions import NewSubmission, SubmissionResponse
from deps.users import CurActiveUserDep
from deps.submissions import SubmissionCrudDp

router = APIRouter(prefix="/submissions", tags=["submissions"])

@router.post(
    "/new-submission",
    status_code=status.HTTP_200_OK,
    response_model=SubmissionResponse
)
async def new_submission(
    new_sub: NewSubmission,
    currentUser: CurActiveUserDep,
    submission_crud: SubmissionCrudDp,
):
    submission = await submission_crud.new_submission(new_sub)
    return SubmissionResponse(**submission.to_dict())
