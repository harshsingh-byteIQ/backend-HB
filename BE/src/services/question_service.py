from src.schemas.question_schema import Question
from fastapi import HTTPException
from src.schemas.question_schema import Question
from sqlalchemy.orm import Session

def create_question(payload, db: Session):
    try:
        questions = []
        
       
        for q in payload.questions:
          
            if q.is_dropdown and not q.options:
                raise HTTPException(status_code=400, detail="Dropdown questions must have options")

          
            question_type = 'select' if q.is_dropdown else 'text'
            
           
            question = Question(
                content=q.content,
                question_for=q.question_for,
                question_type=question_type, 
                options=q.options if q.is_dropdown else None 
            )
            
            questions.append(question)
        
       
        db.add_all(questions)
        db.commit()

        for q in questions:
            db.refresh(q)
        
        return questions

    except Exception as e:
        db.rollback()  
        print(e)
        raise HTTPException(status_code=500, detail="An error occurred while creating questions.")


def delete_respective_question(question_id: int, db: Session):
    try:
        question = db.query(Question).filter(Question.question_id == question_id).first()
        if not question:
            raise HTTPException(status_code=404, detail="Question not found")
        
        db.delete(question)
        db.commit()
        return {"message": f"Question with ID {question_id} deleted successfully"}

    except Exception as e:
        db.rollback()  
        print(e)
        raise HTTPException(status_code=500, detail="An error occurred while deleting the question.")
        
def get_all_question(db: Session):
    try:
      
        questions = db.query(Question).all()
        
        if not questions:
            raise HTTPException(status_code=404, detail="No questions found")
        
        return questions

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="An error occurred while fetching questions.")

def get_all_question_by_role(role , db: Session):
    try:
      
        questions = db.query(Question).filter(Question.question_for == role)
        
        if not questions:
            raise HTTPException(status_code=404, detail="No questions found")
        
        return questions

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="An error occurred while fetching questions.")
             