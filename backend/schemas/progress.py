from pydantic import BaseModel

class UserProgress(BaseModel):
    user_id: int
    station_id: int
    completed: bool
    score: int
