from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.schemas.question_schema import Question
from src.services.question_service import create_question, delete_respective_question
from src.utils.database import get_db
from src.models.question_modals import QuestionBulkCreate , QuestionOut

QuestionRoute = APIRouter()

@QuestionRoute.post("/questions/", response_model=list[QuestionOut])
def create_questions(payload: QuestionBulkCreate, db: Session = Depends(get_db)):
    return create_question(payload, db)

@QuestionRoute.delete("/questions/{question_id}")
def delete_question(question_id: int, db: Session = Depends(get_db)):
    return delete_respective_question(question_id, db)


@QuestionRoute.get("/questions/", response_model=list[QuestionOut])
def get_all_questions(db: Session = Depends(get_db)):
    return db.query(Question).all()