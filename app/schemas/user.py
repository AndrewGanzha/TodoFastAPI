from pydantic import BaseModel, EmailStr

class UserRegisterIn(BaseModel):
    email: EmailStr
    password: str

class LoginIn(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"