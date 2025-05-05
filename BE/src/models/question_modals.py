from pydantic import BaseModel
from typing import List, Optional

class QuestionCreate(BaseModel):
    content: str
    question_for: str
    is_dropdown: bool = False  
    options: Optional[List[str]] = None 
    
    class Config:
     
        @staticmethod
        def validate_options(cls, values):
            if values.get('is_dropdown') and not values.get('options'):
                raise ValueError('Dropdown questions must have options')
            if not values.get('is_dropdown') and values.get('options'):
                raise ValueError('Non-dropdown questions should not have options')
            return values


class QuestionOut(BaseModel):
    question_id: int
    content: str
    question_for: str
    question_type: str
    options: Optional[List[str]] = None  

    class Config:
        
        from_attributes = True

class QuestionBulkCreate(BaseModel):
    questions: List[QuestionCreate]
