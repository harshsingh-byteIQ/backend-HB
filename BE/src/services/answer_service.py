from src.models.answer_modals import AnswerOut, AnswerCreate
from fastapi import HTTPException 
from src.schemas.answer_schema import Answer
from src.schemas.question_schema import Question

def submitted_answer(payload , db):
    try:
        for q in payload.answer:  
            question = db.query(Question).filter(Question.question_id == q.question_id).first()
            answer = db.query(Answer).filter(Answer.question_id == q.question_id and Answer.user_id == q.user_id).first()
            print(q.user_id , Answer.user_id)
            if not question:
                raise HTTPException(status_code=404, detail="Question does not exist")
            else:
                new_answer = Answer(
                question_id=q.question_id,
                user_id=q.user_id,
                answer=q.answer)
                db.add(new_answer)
                db.commit()
                db.refresh(new_answer)
                
        return {"message" :"answer submitted successfully" , "status_code" : 200 , "data" : []}
    except Exception as e:
        print(e)
        
def get_answer(db):
    try:
        all_answer = db.query(Answer).all()
        return all_answer
    except Exception as e:
        print(e) 
            
def delete_answer(id , db):
    try:
        answer = db.query(Answer).filter(Answer.answer_id == id).first()
        if not answer:
            raise HTTPException(status_code=404, detail="Answer does not exist")
        else :
            db.delete(answer)
            db.commit()
        return {"answer deleted successfully"}
    except Exception as e:
        print(e)
                