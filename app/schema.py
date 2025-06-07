from pydantic import BaseModel, EmailStr

class new_user_credentials(BaseModel):
    """data provided by new user to create a new account on this api"""
    
    name: str
    role: str
    email: EmailStr
    password: str


class user_login(BaseModel):
    """Existing user credentials while login"""
    
    email: EmailStr
    password: str


class gym_status_update(BaseModel):
    """Master update the status"""
    
    status: str