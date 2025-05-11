from pydantic import BaseModel, EmailStr
from fastapi import Form 

class UserLogin(BaseModel):
    login_field: str        # user_name hoặc email
    password: str

class RegisterForm(BaseModel):
    name: str
    dob: str
    username: str
    email: EmailStr
    password: str
    
class ChatRequest(BaseModel):
    query: str