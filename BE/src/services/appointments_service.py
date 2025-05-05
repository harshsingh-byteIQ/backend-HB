from src.schemas.appointments_schema import Appointments
from src.models.appointment_modals import Appointment , AppointmentUpdateData
from src.schemas.appointments_schema import AppointmentState
from datetime import datetime
from src.schemas.database_schema import User
import httpx

def send_email_notification(username: str, email: str):
    email_payload = {
        "username": username,
        "email": email,
    }
    try:
        response = httpx.post("http://localhost:8002/appointment-schedule-email", json=email_payload)
        response.raise_for_status()
    except Exception as email_err:
        print(f"Email service failed: {email_err}")

def get_appointments(db):
    try:
        result = []
        existing_user = db.query(Appointments).all()
        
        for user in existing_user:
            user_data = db.query(User).filter(user.requested_to == User.id).first()
            new_user = user.__dict__.copy()
            new_user.pop("_sa_instance_state", None)
            if user_data :
                new_user['last_name'] = user_data.last_name
                new_user['first_name'] = user_data.first_name
                new_user['user_id'] = user_data.id
            
            result.append(new_user)    
        return result
    except Exception as e:
        print(e)
        
def get_scheduled_appointments(db):
    try:
        result = []
        appointments = db.query(Appointments).all()
        
        for slots in appointments:
            requested_to_user_data = db.query(User).filter(int(slots.requested_to) == User.id).first()
            requested_by_user_data = db.query(User).filter(int(slots.requested_by) == User.id).first()
            new_user = slots.__dict__.copy()
            print(new_user)
            new_user.pop("_sa_instance_state", None)
            if requested_to_user_data and requested_by_user_data:
                new_user['last_name_requested'] = requested_to_user_data.last_name
                new_user['first_name_requested'] = requested_to_user_data.first_name
                new_user['user_id_requested'] = requested_to_user_data.id
                new_user['last_name_requested_by'] = requested_by_user_data.last_name
                new_user['first_name_requested_by'] = requested_by_user_data.first_name
                new_user['user_id_requested_by'] = requested_by_user_data.id  
            
            result.append(new_user)
        print(result)        
        return result
    except Exception as e:
        print(e)
            
def appointments_by_role(role , db):
    try:
        result = []
        appointments = db.query(Appointments).all()
        
        for slots in appointments:
            requested_to_user_data = None
            if hasattr(slots, "requested_to") and isinstance(slots.requested_to, str) and slots.requested_to.isdigit():
                requested_to_user_data = db.query(User).filter(User.id == int(slots.requested_to)).first()

            requested_by_user_data = None
            if hasattr(slots, "requested_by") and isinstance(slots.requested_by, str) and slots.requested_by.isdigit():
                requested_by_user_data = db.query(User).filter(User.id == int(slots.requested_by)).first()

            new_user = slots.__dict__.copy()
            new_user.pop("_sa_instance_state", None)
            if requested_to_user_data and requested_by_user_data:
                new_user['last_name'] = requested_to_user_data.last_name if role == "patient" else requested_by_user_data.last_name
                new_user['first_name'] = requested_to_user_data.first_name if role == "patient" else requested_by_user_data.first_name
                new_user['user_id'] = requested_to_user_data.id if role == "patient" else requested_by_user_data.id
            
            result.append(new_user)
        print(result)        
        return result
    except Exception as e:
        print(e)

        
def create_new_appointments(appointment: Appointment, db, background_tasks):
    try:
        user_one = db.query(User).filter(User.id == appointment.requested_to).first()
        user_two = db.query(User).filter(User.id == appointment.requested_by).first()
        
        if user_one and user_two:
            background_tasks.add_task(send_email_notification, user_two.first_name, user_one.email)    
            background_tasks.add_task(send_email_notification, user_one.first_name, user_two.email)

        start_time_str = appointment.time_slot.split(" - ")[0]
        start_datetime = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M")
        
        new_appointment = Appointments(
            status=AppointmentState.scheduled.value,
            requested_by=appointment.requested_by,
            requested_to=appointment.requested_to,
            date=start_datetime,
            time_slot=appointment.time_slot,
        )
        
        db.add(new_appointment)
        db.commit()
        db.refresh(new_appointment)
        return {"message": "Appointment registered successfully"}
    
    except Exception as e:
        return {"error": str(e)}

                                      
def update_appointments_by_id(update_data : AppointmentUpdateData , db):
    try:
        user = db.query(Appointments).filter(Appointments.id == update_data.id).first()
        print(update_data.requested_to)
        if user:
            user.requested_to = update_data.requested_to
            user.status = AppointmentState.assigned.value
            db.commit()
            db.refresh(user)
        return "updated the record"
    except Exception as e:
        print(e)  
                    
def get_appointment_data_details(id , db):
    return {}

def delete_appointment_by_id(id , db):
    try:
        appointment = db.query(Appointments).filter(Appointments.id == id).first()
        if appointment:
            db.delete(appointment)
            db.commit()
            return "Appointment deleted successfully"
        else:
            return "Appointment not found"
    except Exception as e:
        print(e)
        return "Error deleting appointment"

def create_by_request(appointment , db):
    try:
        new_appointment = Appointments(
            status=AppointmentState.assigned.value,            
            requested_by=appointment.requested_by, 
            time_slot="",
        )
        db.add(new_appointment)
        db.commit()
        db.refresh(new_appointment)
        return {"message": "Appointment registered successfully"}
    except Exception as e:
        return {"error" , e}

def get_requested_appointment(id , db):
    try:
        result = []
        requested_appointments = db.query(Appointments).filter(Appointments.status == AppointmentState.assigned.name).all()
        for user in requested_appointments:
            user_data = db.query(User).filter(user.requested_by == User.id).first()
            new_user = user.__dict__.copy()
            new_user.pop("_sa_instance_state", None)
            if user_data :
                new_user['last_name'] = user_data.last_name
                new_user['first_name'] = user_data.first_name
                new_user['user_id'] = user_data.id
            
            result.append(new_user)    
        return result
    except Exception as e:
        print(e)     