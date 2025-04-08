from pydantic import BaseModel

class user_data(BaseModel):
    access_token : str
    role : str