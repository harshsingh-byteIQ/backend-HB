from pydantic import BaseModel
from typing import List

class AnswerCreate(BaseModel):
    question_id: int
    user_id: int
    answer: str

class AnswerOut(BaseModel):
    answer_id: int
    question_id: int
    user_id: int
    answer: str

    model_config = {
        "from_attributes": True
    }

