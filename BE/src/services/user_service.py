from src.schemas.database_schema import User
from src.utils.response_body import success_response , error_response
from fastapi import HTTPException
from src.schemas.answer_schema import Answer
from src.schemas.question_schema import Question
from src.schemas.appointments_schema import Appointments
from datetime import datetime, timedelta

def get_user_details(id, db):
    user = db.query(User).filter(User.id == id).first()
    try:
        user_data = {
            "first_name": user.first_name ,
            "last_name": user.last_name,
            "email": user.email,
            "contact_no":user.contact_no,
            "role":user.role,
        }
        return success_response(user_data , "Data fetched Successfully " , 200)
    except Exception as e:
        print(e)

def delete_user(id , db):
    user = db.query(User).filter(User.id == id).first()
    try:
        if user:
            db.delete(user)
            db.commit()
            return success_response({}, "User deleted successfully", 200)
        else:
            return success_response({}, "User not found", 404)
    except Exception as e:
        return error_response({}, "An error occurred while deleting the user", 500)     

def get_users(role, id, db):
    try:
        users = db.query(User).filter(User.role == role).all()
        patient_answer = db.query(Answer).filter(Answer.user_id == id).all()

        patient_answers_dict = {
            a.question_id: str(a.answer).strip().lower()
            for a in patient_answer
        }
        
        result = []

        for user in users:
            user_dict = user.__dict__.copy()
            user_dict.pop("_sa_instance_state", None)
            user_dict.pop("password", None)

            user_id = str(user.id) if user.id is not None else None
            if not user_id or user_id == "undefined":
                continue

            user_answers = db.query(Answer).filter(Answer.user_id == user_id).all()

            student_answers_dict = {
                a.question_id: str(a.answer).strip().lower()
                for a in user_answers
            }
          
            overlapping_qids = [qid for qid in patient_answers_dict if qid in student_answers_dict]
            total_questions = len(overlapping_qids)

            match_score = 0
            for qid in overlapping_qids:
                user_ans = student_answers_dict[qid]
                patient_ans = patient_answers_dict[qid]

                if user_ans == patient_ans:
                    match_score += 1

            score_percentage = (match_score / total_questions) * 100 if total_questions else 0
            user_dict["score"] = round(score_percentage, 2)


            if "selected_slots" in user_dict and user_dict["selected_slots"]:
                appointments = db.query(Appointments).filter(Appointments.requested_to == user_id).all()

                booked_dates = {
                    appointment.date.date() if hasattr(appointment.date, "date") else appointment.date
                    for appointment in appointments
                } if appointments else set()

                updated_slots = []
                for slot in user_dict["selected_slots"]:
                    next_date = get_next_available_date(
                        day=slot["day"],
                        start_time=slot["startTime"],
                        end_time=slot["endTime"],
                        booked_dates=booked_dates
                    )
                    updated_slot = slot.copy()
                    updated_slot["next_available_date"] = next_date
                    updated_slots.append(updated_slot)

                user_dict["selected_slots"] = updated_slots

            result.append(user_dict)

        return result

    except Exception as e:
        import traceback
        traceback.print_exc()
        return []

def get_next_available_date(day, start_time, end_time, booked_dates):
    """
    Find the next available date for a slot with the same day, start time, and end time,
    including today if the time has not passed.
    """
    day_map = {
        "Monday": 0, "Tuesday": 1, "Wednesday": 2,
        "Thursday": 3, "Friday": 4, "Saturday": 5, "Sunday": 6
    }

    day_num = day_map.get(day)
    if day_num is None:
        return None

    today = datetime.now().date()
    now = datetime.now()

    today_weekday = today.weekday()

    # Calculate time objects from string
    try:
        end_time_obj = datetime.strptime(end_time, "%H:%M").time()
    except ValueError:
        return None  # invalid time format

    # Check if today is the correct day and time has not passed
    if today_weekday == day_num:
        if now.time() < end_time_obj and today not in booked_dates:
            return today.strftime("%Y-%m-%d")

    # Otherwise, find the next date
    days_ahead = (day_num - today_weekday + 7) % 7 or 7
    next_date = today + timedelta(days=days_ahead)

    while next_date in booked_dates:
        next_date += timedelta(days=7)

    return next_date.strftime("%Y-%m-%d")

def get_user_details_with_answer (id , db):
    user = db.query(User).filter(User.id == id).first()
    answer = db.query(Answer).filter(Answer.user_id == id).all()
    try:
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        question = db.query(Question).filter(Question.question_for == "both").all()
        answers_data = [
            {
                "question_id": a.question_id,
                "answer": a.answer,
                "user_id": a.user_id, 
            }
            for a in answer
        ]
        question_data = [ {"question_id": a.question_id,"content": a.content}  for a in question]
        merged_data = [
        {
            "question_id": a["question_id"],
            "answer": a["answer"],
            "user_id": a["user_id"],
            "content": next((q["content"] for q in question_data if q["question_id"] == a["question_id"]), None)  # Find the content for the answer
        }
            for a in answers_data
        ]
        user_data = {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "contact_no": user.contact_no,
            "role": user.role,
            "q_n_a_data": merged_data,
        }

        return success_response(user_data, "Data retrieved successfully", 200)
    except Exception as e:
        db.rollback()  
        print(e)
        raise HTTPException(status_code=500, detail="An error occurred while featching data.")    
              
def get_perfect_candidate(id, db):
    try:
        users = db.query(User).filter(User.role == "student").all()
        patient_answer = db.query(Answer).filter(Answer.user_id == id).all()

        patient_answers_dict = {
            a.question_id: str(a.answer).strip().lower()
            for a in patient_answer
        }

        candidates = []

        for user in users:
            user_dict = user.__dict__.copy()
            user_dict.pop("_sa_instance_state", None)
            user_dict.pop("password", None)

            user_id = str(user.id) if user.id is not None else None
            if not user_id or user_id == "undefined":
                continue

            user_answers = db.query(Answer).filter(Answer.user_id == user_id).all()

            student_answers_dict = {
                a.question_id: str(a.answer).strip().lower()
                for a in user_answers
            }

            overlapping_qids = [qid for qid in patient_answers_dict if qid in student_answers_dict]
            total_questions = len(overlapping_qids)

            match_score = 0
            for qid in overlapping_qids:
                if student_answers_dict[qid] == patient_answers_dict[qid]:
                    match_score += 1

            score_percentage = (match_score / total_questions) * 100 if total_questions else 0
            score_val = round(score_percentage, 2)
            user_dict["score"] = score_val
          
            if "selected_slots" in user_dict and user_dict["selected_slots"]:
                appointments = db.query(Appointments).filter(Appointments.requested_to == user_id).all()
                booked_dates = {
                    appointment.date.date() if hasattr(appointment.date, "date") else appointment.date
                    for appointment in appointments
                } if appointments else set()

                updated_slots = []
                for slot in user_dict["selected_slots"]:
                    next_date = get_next_available_date(
                        day=slot["day"],
                        start_time=slot["startTime"],
                        end_time=slot["endTime"],
                        booked_dates=booked_dates
                    )
                    updated_slot = slot.copy()
                    updated_slot["next_available_date"] = next_date
                    updated_slots.append(updated_slot)

                user_dict["selected_slots"] = updated_slots

            candidates.append(user_dict)

        top_candidates = sorted(candidates, key=lambda x: x["score"], reverse=True)[:3]
        return top_candidates

    except Exception as e:
        import traceback
        traceback.print_exc()
        return []
