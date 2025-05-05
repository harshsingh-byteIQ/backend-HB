from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.utils.database import get_db
from src.services.appointments_service import get_appointments , create_new_appointments ,update_appointments_by_id , delete_appointment_by_id , create_by_request , get_requested_appointment , get_scheduled_appointments  , appointments_by_role
from src.models.appointment_modals import Appointment , AppointmentUpdateData
from fastapi import BackgroundTasks

Appointment_route = APIRouter()

@Appointment_route.get("/get-appointments")
def get_all_appointments(db:Session = Depends(get_db)):
    return get_appointments(db)

@Appointment_route.post("/create-appointments")
def create_appointments(appointment: Appointment, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    return create_new_appointments(appointment, db, background_tasks)

@Appointment_route.post("/create-appointments-by-request")
def create_appointments_by_request(appointment: Appointment, db: Session = Depends(get_db)):
    return create_by_request(appointment, db)

@Appointment_route.put("/update-appointments")
def update_appointments(update_data : AppointmentUpdateData  ,db:Session = Depends(get_db)):
    return update_appointments_by_id(update_data , db)

@Appointment_route.delete("/delete-appointment/{id}")
def delete_appointment(id = id, db : Session = Depends(get_db)):
    return delete_appointment_by_id(id , db)

@Appointment_route.get("/get-appointment-requests/{id}")
def get_requested_appointments(id = id , db :Session = Depends(get_db)):
    return get_requested_appointment(id,db)

@Appointment_route.get("/schedule-appointments")
def get_scheduled_appointment(db:Session = Depends(get_db)):
    return get_scheduled_appointments(db)

@Appointment_route.get('/appointment-by-role/{role}')
def get_appointments_by_role(role : str , db:Session = Depends(get_db)):
    return appointments_by_role(role , db)


