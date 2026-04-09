from fastapi import APIRouter
from services.leaderboard_service import LeaderboardService

router = APIRouter()

@router.get("/leaderboard")
async def get_leaderboard(limit: int = 10):
    return LeaderboardService.get_leaderboard(limit)
