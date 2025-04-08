from src.models.auth_modals import UserLogin
from src.models.auth_modals import UserRegister
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.utils.database import get_db
from src.services.auth_service import register_user , get_user , verify_user

AuthRoute = APIRouter()

@AuthRoute.post("/register")
def register(user: UserRegister, db: Session = Depends(get_db)):
    return register_user(user = user,  db = db)

@AuthRoute.post("/login")
def login_user(login_data: UserLogin, db: Session = Depends(get_db)):
    return verify_user(login_data = login_data , db = db)

@AuthRoute.get("/all-user")
def get_all_user(db:Session = Depends(get_db)):
    return get_user(db)
