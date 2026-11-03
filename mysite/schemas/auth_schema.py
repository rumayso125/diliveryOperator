from pydantic import BaseModel, EmailStr
from datetime import date


class UserProfileRegisterSchema(BaseModel):
    username: str
    email: EmailStr
    phone_number: str
    password: str


class UserProfileLoginSchema(BaseModel):
    username: str
    password: str


class UserProfileUpdateSchema(BaseModel):
    username: str
    email: EmailStr
    phone_number: str


class UserProfileOutputSchema(BaseModel):
    id: int
    username: str
    email: EmailStr
    phone_number: str
    registered_date: date