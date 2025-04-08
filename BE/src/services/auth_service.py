from src.schemas.database_schema import User
from fastapi import HTTPException
from src.utils.manageTokens import hash_password , verify_password , create_access_token
from datetime import datetime
from src.models.auth_modals import UserLogin
from src.utils.response_body import error_response , success_response

def register_user(user , db):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    try:
        hashed_password = hash_password(user.password)

        new_user = User(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            contact_no=user.contact_no,
            password=hashed_password,
            created_at=datetime.utcnow(),
            role=user.role
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {"message": "User registered successfully"}
    except Exception as e:
         return error_response(error=e.detail , message="something went wrong" , status_code = e.status_code)

def get_user(db):
    try:
        existing_user = db.query(User).all()
        result = []
        for user in existing_user:
            user_dict = user.__dict__.copy()
            user_dict.pop("_sa_instance_state", None) 
            user_dict.pop("password", None)            
            result.append(user_dict)

        return result
    except Exception as e:
        print(e)    

def verify_user(login_data : UserLogin , db):
    user = db.query(User).filter(User.email == login_data.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found. Please register.")
    
    if not verify_password(login_data.password, user.password):
        raise HTTPException(status_code=401, detail="Incorrect password. Please try again.")
    try:

        token = create_access_token(user.email)
        data = {"access_token": token , "role":user.role , "id" : user.id}
        return success_response(data , "Login successfull" , 200)
    except Exception as e:
        return error_response(error=e.detail , message="something went wrong" , status_code = e.status_code)           