from src.models.answer_modals import AnswerOut, AnswerCreate
from fastapi import FastAPI, Depends, HTTPException , APIRouter
from sqlalchemy.orm import Session
from src.schemas.answer_schema import Answer
from src.schemas.question_schema import Question
from src.services.answer_service import submitted_answer
from src.utils.database import get_db

AnswerRoute = APIRouter()

@AnswerRoute.post("/answers/", response_model=AnswerOut)
def submit_answer(payload: AnswerCreate, db: Session = Depends(get_db)):
    return submitted_answer(payload, db)