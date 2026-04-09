from pydantic import BaseModel
from typing import List, Optional

class Station(BaseModel):
    id: int
    name: str
    content: str
    position: int

class StationCreate(BaseModel):
    name: str
    content: str
    position: int

class StationUpdate(BaseModel):
    name: str
    content: str
    position: int

class Question(BaseModel):
    id: int
    station_id: int
    question: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    correct_answer: str

class AnswerSubmit(BaseModel):
    user_id: int
    station_id: int
    question_id: int
    answer: str
