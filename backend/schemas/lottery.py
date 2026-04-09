from pydantic import BaseModel

class LotteryRequest(BaseModel):
    user_id: int

class LotteryEntry(BaseModel):
    user_id: int
    name: str
    phone: str
    address: str
