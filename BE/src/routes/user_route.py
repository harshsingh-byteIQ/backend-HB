from src.models.user_modals import user_data
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.utils.database import get_db
from src.services.user_service import get_user_details , delete_user

UserRoute = APIRouter()

@UserRoute.get("/get-user-data/{id}")
def get_all_user(id = id ,db:Session = Depends(get_db)):
    return get_user_details(id ,db)

@UserRoute.delete("/delete-user/{id}")
def delete_user_by_id(id = id , db : Session = Depends(get_db)):
    return delete_user(id , db)