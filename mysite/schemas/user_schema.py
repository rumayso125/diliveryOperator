from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional


class UserProfileInputSchema(BaseModel):
    username: str
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    password: str


class UserProfileUpdateSchema(BaseModel):
    username: str
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    password: Optional[str] = None  # если не передан, пароль не меняется


class UserProfileOutputSchema(BaseModel):
    id: int
    username: str
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    registered_date: date
