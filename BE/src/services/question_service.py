from src.schemas.question_schema import Question
from fastapi import HTTPException

def create_question(payload, db):
    try:
        questions = [Question(content=q.content) for q in payload.questions]
        db.add_all(questions)
        db.commit()
        for q in questions:
            db.refresh(q)
        return questions
    except Exception as e:
        print(e)

def delete_respective_question(question_id, db):
    try:
        question = db.query(Question).filter(Question.question_id == question_id).first()
        if not question:
            raise HTTPException(status_code=404, detail="Question not found")
        db.delete(question)
        db.commit()
        return {"message": "Question deleted successfully"}
    except Exception as e:
        print(e)