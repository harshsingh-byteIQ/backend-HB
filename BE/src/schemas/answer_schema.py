from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

AnswerBase = declarative_base()

class Answer(AnswerBase):
    __tablename__ = "answers"

    answer_id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    answer = Column(String, nullable=False)
