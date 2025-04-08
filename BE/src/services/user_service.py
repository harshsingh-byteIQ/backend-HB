from src.schemas.database_schema import User
from src.utils.response_body import success_response , error_response

def get_user_details(id, db):
    user = db.query(User).filter(User.id == id).first()
    try:
        user_data = {
            "first_name": user.first_name ,
            "last_name": user.last_name,
            "email": user.email,
            "contact_no":user.contact_no,
            "role":user.role,
        }
        return success_response(user_data , "Data fetched Successfully " , 200)
    except Exception as e:
        print(e)


def delete_user(id , db):
    user = db.query(User).filter(User.id == id).first()
    try:
        if user:
            db.delete(user)
            db.commit()
            return success_response({}, "User deleted successfully", 200)
        else:
            return success_response({}, "User not found", 404)
    except Exception as e:
        return error_response({}, "An error occurred while deleting the user", 500)        