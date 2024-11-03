from fastapi import APIRouter, status, Response
from shemas.submissions import NewSubmission, SubmissionResponse
from deps.users import CurActiveUserDep
from deps.submissions import SubmissionCrudDp
from rabbit.pub import pub_m
from rabbit.get_result import get_submission_result

router = APIRouter(prefix="/submissions", tags=["submissions"])


@router.post(
    "/new-submission", status_code=status.HTTP_200_OK, response_model=SubmissionResponse
)
async def new_submission(
    new_sub: NewSubmission,
    currentUser: CurActiveUserDep,
    submission_crud: SubmissionCrudDp,
):
    submission = await submission_crud.new_submission(new_sub)
    await pub_m(submission.submission_id, currentUser.id)
    return SubmissionResponse(**submission.to_dict())


@router.get("/check-submission/{submission_id}")
async def get_test(submission_id: int, current_user: CurActiveUserDep, submission_crud: SubmissionCrudDp):
    status = await get_submission_result(current_user.id, submission_id)
    submission = await submission_crud.set_submission_status(submission_id, status)
    return SubmissionResponse(**submission.to_dict())
