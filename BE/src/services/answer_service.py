from src.models.answer_modals import AnswerOut, AnswerCreate
from fastapi import FastAPI, Depends, HTTPException , APIRouter
from sqlalchemy.orm import Session
from src.schemas.answer_schema import Answer
from src.schemas.question_schema import Question

def submitted_answer(payload , db):
    try:
        question = db.query(Question).filter(Question.question_id == payload.question_id).first()
        if not question:
            raise HTTPException(status_code=404, detail="Question does not exist")

        new_answer = Answer(
            question_id=payload.question_id,
            user_id=payload.user_id,
            answer=payload.answer
        )
        db.add(new_answer)
        db.commit()
        db.refresh(new_answer)
        return new_answer
    except Exception as e:
        print(e)