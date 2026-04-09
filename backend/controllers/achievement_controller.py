from fastapi import APIRouter
from services.achievement_service import AchievementService

router = APIRouter()

@router.get("/user-achievements/{user_id}")
async def get_user_achievements(user_id: int):
    return AchievementService.get_user_achievements(user_id)
