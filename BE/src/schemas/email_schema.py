from pydantic import BaseModel


class AdminEmailRequest(BaseModel):
    username: str
    email: str
    password: str

class appointment_schedule_request_patient(BaseModel):
    username: str
    email: str
