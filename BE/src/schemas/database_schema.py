from sqlalchemy import Column, Integer, String, Enum, DateTime , JSON
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy.orm import relationship
import enum
from typing import List , Dict
from sqlalchemy import Column, Integer, String, Enum as SQLAlchemyEnum, ForeignKey, DateTime , ARRAY,  func

Base = declarative_base()

class UserRole(enum.Enum):
    admin = "admin"
    student = "student"
    caretaker = "caretaker"
    patient = "patient"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    contact_no = Column(String, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    role = Column(Enum(UserRole), nullable=False)  # Enum field
    selected_slots = Column(JSON, nullable=True)
    
