from fastapi import APIRouter, Depends, HTTPException
from schemas.lottery import LotteryRequest, LotteryEntry
from services.lottery_service import LotteryService
from common.jwt_utils import get_current_user

router = APIRouter()

@router.post("/lottery")
async def lottery(request: LotteryRequest, current_user: dict = Depends(get_current_user)):
    user_id = request.user_id
    
    # 验证用户权限
    if current_user['id'] != user_id:
        raise HTTPException(status_code=403, detail="无权操作")
    
    return LotteryService.perform_lottery(user_id)

@router.post("/submit-address")
async def submit_address(entry: LotteryEntry, current_user: dict = Depends(get_current_user)):
    # 验证用户权限
    if current_user['id'] != entry.user_id:
        raise HTTPException(status_code=403, detail="无权操作")
    
    return LotteryService.submit_address(
        entry.user_id,
        entry.name,
        entry.phone,
        entry.address
    )

@router.get("/export-winners")
async def export_winners():
    return LotteryService.export_winners()

@router.get("/lottery-result/{user_id}")
async def get_lottery_result(user_id: int, current_user: dict = Depends(get_current_user)):
    # 验证用户权限
    if current_user['id'] != user_id:
        raise HTTPException(status_code=403, detail="无权操作")
    
    return LotteryService.get_lottery_result(user_id)
