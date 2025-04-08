from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.utils.database import get_db
from src.services.appointments_service import get_appointments , create_new_appointments ,update_appointments_by_id , delete_appointment_by_id
from src.models.appointment_modals import Appointment , AppointmentUpdateData

Appointment_route = APIRouter()

@Appointment_route.get("/get-appointments")
def get_all_appointments(db:Session = Depends(get_db)):
    return get_appointments(db)

@Appointment_route.post("/create-appointments")
def create_appointments(appointment : Appointment ,db:Session = Depends(get_db)):
    return create_new_appointments(appointment , db)

@Appointment_route.put("/update-appointments")
def update_appointments(update_data : AppointmentUpdateData  ,db:Session = Depends(get_db)):
    return update_appointments_by_id(update_data , db)

@Appointment_route.delete("/delete-appointment/{id}")
def delete_appointment(id = id, db : Session = Depends(get_db)):
    return delete_appointment_by_id(id , db)


@Appointment_route.get("/get-appointment-data-with-user/{id}")
def get_appointment_data_with_user(id = id, db : Session = Depends(get_db)):
    return get_appointment_data_details(id , db)