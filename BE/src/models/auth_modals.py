from pydantic import BaseModel,EmailStr
from typing import Any, Optional, Union , List , Dict
from enum import Enum

class UserLogin(BaseModel):
    email: str
    password: str
    
class UserRole(str, Enum):
    admin = "admin"
    student = "student"
    caretaker = "caretaker"
    patient = "patient"

DEFAULT_SLOTS = [
        {
        "day" : '',
        "startTime" : '',
        "endTime" : '',
    }]

class UserRegister(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    contact_no: str
    password: str
    role: UserRole
    selected_slots : Optional[List[Dict[str,str]]] = DEFAULT_SLOTS
    
class TokenData(BaseModel):
    email: str    
    
class BaseResponseModel(BaseModel):
    status_code: int
    message: str   

class SuccessResponseModal(BaseResponseModel):
    data: Optional[Any] = None   

class ErrorResponseModal(BaseResponseModel):
    error: Optional[Union[str, dict]] = None         
    