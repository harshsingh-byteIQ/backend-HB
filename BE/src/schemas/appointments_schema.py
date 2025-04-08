from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Enum, DateTime
from datetime import datetime
import enum

AppointmentBase = declarative_base()

class AppointmentState(enum.Enum):
    initiated = "initiated"
    assigned = "assigned"
    scheduled = "scheduled"

class Appointments(AppointmentBase):
    __tablename__ = "appointments"
    
    id = Column(Integer , primary_key = True , index=True)
    status = Column(String , nullable=False)
    requested_by = Column(String , nullable=False)
    requested_to = Column(String)
    date = Column(DateTime , default=datetime.utcnow)
    time_slot = Column(String)

class Appointments_details(AppointmentBase):
    __tablename__ = "Appointments_details"   
    
    id = Column(Integer , primary_key = True , index = True)
    