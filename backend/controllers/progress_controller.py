from fastapi import APIRouter, Depends, HTTPException
from schemas.station import AnswerSubmit
from services.progress_service import ProgressService
from common.jwt_utils import get_current_user

router = APIRouter()

@router.get("/user-progress/{user_id}")
async def get_user_progress(user_id: int):
    return ProgressService.get_user_progress(user_id)

@router.post("/submit-answer")
async def submit_answer(submission: AnswerSubmit, current_user: dict = Depends(get_current_user)):
    # 验证用户权限
    if current_user['id'] != submission.user_id:
        raise HTTPException(status_code=403, detail="无权操作")
    
    return ProgressService.submit_answer(
        submission.user_id,
        submission.station_id,
        submission.question_id,
        submission.answer
    )
