from fastapi import APIRouter, HTTPException, Depends
from services.admin_service import AdminService
from schemas.user import UserCreate
from schemas.station import StationCreate, StationUpdate
from schemas.achievement import AchievementCreate
from common.jwt_utils import get_current_admin
from pydantic import BaseModel

router = APIRouter(prefix="/admin", tags=["admin"])

# Pydantic models for request bodies
class PrizeCreate(BaseModel):
    name: str
    level: int
    probability: float
    description: str

class QuestionCreate(BaseModel):
    station_id: int
    question: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    correct_answer: str
    score: int

# 站点管理
@router.get("/stations")
async def get_all_stations(current_admin: dict = Depends(get_current_admin)):
    return AdminService.get_all_stations()

@router.post("/stations")
async def create_station(station: StationCreate, current_admin: dict = Depends(get_current_admin)):
    return AdminService.create_station(station.name, station.content, station.position)

@router.put("/stations/{station_id}")
async def update_station(station_id: int, station: StationUpdate, current_admin: dict = Depends(get_current_admin)):
    return AdminService.update_station(station_id, station.name, station.content, station.position)

@router.delete("/stations/{station_id}")
async def delete_station(station_id: int, current_admin: dict = Depends(get_current_admin)):
    return AdminService.delete_station(station_id)

# 问题管理
@router.get("/questions")
async def get_all_questions(current_admin: dict = Depends(get_current_admin)):
    return AdminService.get_all_questions()

@router.post("/questions")
async def create_question(question_data: QuestionCreate, current_admin: dict = Depends(get_current_admin)):
    return AdminService.create_question(
        question_data.station_id, 
        question_data.question, 
        question_data.option_a, 
        question_data.option_b, 
        question_data.option_c, 
        question_data.option_d, 
        question_data.correct_answer, 
        question_data.score
    )

@router.put("/questions/{question_id}")
async def update_question(question_id: int, question_data: QuestionCreate, current_admin: dict = Depends(get_current_admin)):
    return AdminService.update_question(
        question_id, 
        question_data.question, 
        question_data.option_a, 
        question_data.option_b, 
        question_data.option_c, 
        question_data.option_d, 
        question_data.correct_answer, 
        question_data.score
    )

@router.delete("/questions/{question_id}")
async def delete_question(question_id: int, current_admin: dict = Depends(get_current_admin)):
    return AdminService.delete_question(question_id)

# 成就管理
@router.get("/achievements")
async def get_all_achievements(current_admin: dict = Depends(get_current_admin)):
    return AdminService.get_all_achievements()

@router.post("/achievements")
async def create_achievement(achievement: AchievementCreate, current_admin: dict = Depends(get_current_admin)):
    return AdminService.create_achievement(achievement.name, achievement.description, achievement.icon, achievement.condition_type, achievement.condition_value)

@router.put("/achievements/{achievement_id}")
async def update_achievement(achievement_id: int, achievement: AchievementCreate, current_admin: dict = Depends(get_current_admin)):
    return AdminService.update_achievement(achievement_id, achievement.name, achievement.description, achievement.icon, achievement.condition_type, achievement.condition_value)

@router.delete("/achievements/{achievement_id}")
async def delete_achievement(achievement_id: int, current_admin: dict = Depends(get_current_admin)):
    return AdminService.delete_achievement(achievement_id)

# 奖品管理
@router.get("/lottery")
async def get_all_lottery_records(current_admin: dict = Depends(get_current_admin)):
    return AdminService.get_all_lottery_records()

@router.get("/lottery/winners")
async def get_winners(current_admin: dict = Depends(get_current_admin)):
    return AdminService.get_winners()

@router.post("/lottery/winners")
async def set_winner(lottery_id: int, prize: str, current_admin: dict = Depends(get_current_admin)):
    return AdminService.set_winner(lottery_id, prize)

# 奖品级别管理
@router.get("/prizes")
async def get_all_prizes(current_admin: dict = Depends(get_current_admin)):
    return AdminService.get_all_prizes()

@router.post("/prizes")
async def create_prize(prize_data: PrizeCreate, current_admin: dict = Depends(get_current_admin)):
    return AdminService.create_prize(prize_data.name, prize_data.level, prize_data.probability, prize_data.description)

@router.put("/prizes/{prize_id}")
async def update_prize(prize_id: int, prize_data: PrizeCreate, current_admin: dict = Depends(get_current_admin)):
    return AdminService.update_prize(prize_id, prize_data.name, prize_data.level, prize_data.probability, prize_data.description)

@router.delete("/prizes/{prize_id}")
async def delete_prize(prize_id: int, current_admin: dict = Depends(get_current_admin)):
    return AdminService.delete_prize(prize_id)

# 用户管理
@router.get("/users")
async def get_all_users(current_admin: dict = Depends(get_current_admin)):
    return AdminService.get_all_users()

@router.post("/users")
async def create_user(user: UserCreate, current_admin: dict = Depends(get_current_admin)):
    return AdminService.create_user(user.username, user.email, user.password)

@router.put("/users/{user_id}")
async def update_user(user_id: int, user: UserCreate, current_admin: dict = Depends(get_current_admin)):
    return AdminService.update_user(user_id, user.username, user.email, user.password)

@router.delete("/users/{user_id}")
async def delete_user(user_id: int, current_admin: dict = Depends(get_current_admin)):
    return AdminService.delete_user(user_id)
