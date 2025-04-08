from pydantic import BaseModel
from typing import List

class QuestionCreate(BaseModel):
    content: str

class QuestionOut(BaseModel):
    question_id: int
    content: str

    model_config = {
        "from_attributes": True
    }

class QuestionBulkCreate(BaseModel):
    questions: List[QuestionCreate]
