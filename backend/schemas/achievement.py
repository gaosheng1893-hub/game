from pydantic import BaseModel

class Achievement(BaseModel):
    id: int
    name: str
    description: str
    icon: str
    condition_type: str
    condition_value: int

class AchievementCreate(BaseModel):
    name: str
    description: str
    icon: str
    condition_type: str
    condition_value: int

class UserAchievement(BaseModel):
    user_id: int
    achievement_id: int
