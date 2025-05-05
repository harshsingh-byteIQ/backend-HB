from sqlalchemy import Column, Integer, String, Enum, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import validates

QuestionBase = declarative_base()

class Question(QuestionBase):
    __tablename__ = "questions"

    question_id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    question_for = Column(String, nullable=False)
    question_type = Column(Enum('select', 'multiselect', 'text', name='question_type_enum'), nullable=False)
    options = Column(JSON, nullable=True) 

    @validates('options')
    def validate_options(self, key, value):
        if self.question_type in ['select', 'multiselect'] and not isinstance(value, list):
            raise ValueError("Options must be a list when the question type is select or multiselect")
        if self.question_type not in ['select', 'multiselect'] and value is not None:
            raise ValueError("Options should be null for text-based questions")
        return value
