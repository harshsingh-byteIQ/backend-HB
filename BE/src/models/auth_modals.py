from pydantic import BaseModel,EmailStr
from typing import Any, Optional, Union
from enum import Enum

class UserLogin(BaseModel):
    email: str
    password: str
    
class UserRole(str, Enum):
    admin = "admin"
    student = "student"
    caretaker = "caretaker"
    patient = "patient"

class UserRegister(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    contact_no: str
    password: str
    role: UserRole
    
class TokenData(BaseModel):
    email: str    
    
class BaseResponseModel(BaseModel):
    status_code: int
    message: str   

class SuccessResponseModal(BaseResponseModel):
    data: Optional[Any] = None   

class ErrorResponseModal(BaseResponseModel):
    error: Optional[Union[str, dict]] = None         
    