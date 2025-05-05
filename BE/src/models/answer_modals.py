from pydantic import BaseModel
from typing import List

class AnswerCreate(BaseModel):
    question_id: int
    user_id: int
    answer: str

class AnswerOut(BaseModel):
    message : str
    status_code : int 
    data : List
    model_config = {
        "from_attributes": True
    }

class AnswerBulkCreate(BaseModel):
    answer: List[AnswerCreate]