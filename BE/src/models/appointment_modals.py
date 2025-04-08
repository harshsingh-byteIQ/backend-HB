from pydantic import BaseModel
from typing import Optional

class Appointment(BaseModel):
    requested_by: str
    requested_to: Optional[str] = None
    time_slot: str

class AppointmentUpdateData(BaseModel):
    id : int
    requested_to : str