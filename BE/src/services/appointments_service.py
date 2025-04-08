from src.schemas.appointments_schema import Appointments
from src.models.appointment_modals import Appointment , AppointmentUpdateData
from src.schemas.appointments_schema import AppointmentState
from datetime import datetime
from src.schemas.database_schema import User

def get_appointments(db):
    try:
        result = []
        existing_user = db.query(Appointments).all()
        
        for user in existing_user:
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
        
def create_new_appointments(appointment: Appointment, db):
    print(appointment)
    try:
        new_appointment = Appointments(
            status=AppointmentState.initiated.value,            
            requested_by=appointment.requested_by,
            requested_to=appointment.requested_to, 
            date=datetime.utcnow(),
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

        
    

                      