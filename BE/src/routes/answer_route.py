from src.models.answer_modals import AnswerOut, AnswerBulkCreate
from fastapi import FastAPI, Depends, HTTPException , APIRouter
from sqlalchemy.orm import Session
from src.schemas.answer_schema import Answer
from src.schemas.question_schema import Question
from src.services.answer_service import submitted_answer , get_answer , delete_answer
from src.utils.database import get_db

AnswerRoute = APIRouter()

@AnswerRoute.post("/answers/", response_model=AnswerOut)
def submit_answer(payload: AnswerBulkCreate, db: Session = Depends(get_db)):
    return submitted_answer(payload, db)

@AnswerRoute.get("/get-all-answer")
def get_all_answers(db : Session = Depends(get_db)):
    return get_answer(db)

@AnswerRoute.delete("/delete-answer/{id}")
def delete_answer_by_id(id = id , db : Session = Depends(get_db)):
    return delete_answer(id , db)