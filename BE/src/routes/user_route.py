from src.models.user_modals import user_data
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.utils.database import get_db
from src.services.user_service import get_user_details , delete_user , get_users , get_user_details_with_answer , get_perfect_candidate

UserRoute = APIRouter()

@UserRoute.get("/get-user-data/{id}")
def get_all_user(id = id ,db:Session = Depends(get_db)):
    return get_user_details(id ,db)

@UserRoute.delete("/delete-user/{id}")
def delete_user_by_id(id = id , db : Session = Depends(get_db)):
    return delete_user(id , db)

@UserRoute.get("/get-all-user-by-roles/{role}/{id}")
def get_user_by_role(role = str , id = id , db : Session = Depends(get_db)):
    return get_users(role , id , db)

@UserRoute.get("/user-details-with-description/{id}")
def get_user_details_in_depth(id = id , db : Session = Depends(get_db)):
    return get_user_details_with_answer(id , db)

@UserRoute.get("/get-perfect-candidate/{id}")
def perfect_candidate(id = id , db : Session = Depends(get_db)):
    return get_perfect_candidate(id , db)