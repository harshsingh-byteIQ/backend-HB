from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

QuestionBase = declarative_base()

class Question(QuestionBase):
    __tablename__ = "questions"

    question_id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)

