"""
File: user.py
Path: /app/models/user.py
Description: Definition of Fields used on model classes attributes.
CreatedAt: 01/03/2023
"""

# # Installed # #
# from fastapi import status
# from fastapi.responses import JSONResponse
# from fastapi.encoders import jsonable_encoder

from pydantic import BaseModel, Field, validator, EmailStr, constr
import re

class User(BaseModel):
    _id = str
    firstName: str
    lastName: str
    email: EmailStr
    phone: str
    password: str
    startDate: str
    endDate: str

    @validator('firstName')
    def firstName_check(cls, v):
        if not re.match("^\S[A-Za-z@#&$%]{2,9}$", v):
            raise ValueError("Name must be contian 3 to 10 chars")
        return v

    @validator('lastName')
    def lastName_check(cls, v):
        if not re.match("^\S[A-Za-z@#&+-]{2,9}$", v):
            raise ValueError("Name must be contian 3 to 10 chars")
        return v
    
    @validator('email')
    def email_check(cls, v):
        
        if not re.match("^[a-z0-9]+[\._]?[ a-z0-9]+[@]\w+[. ]\w{2,6}$", v):
            raise ValueError("Email is required")
        return v
    
    @validator('phone')
    def phone_check(cls, v):
        
        if not re.match("^[+][0-9]{12}$", v):
            raise ValueError("Phone number is required")
        return v
    
    @validator('password')
    def password_check(cls, v):
        
        if not re.match("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{5,12}$", v):
            raise ValueError("Password is required")
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "firstName":"ticvic",
                "lastName":"ticvic", 
                "email":"ticvic@ticvic.com",
                "phone":"+919843327733",
                "password":"Ticvic@123",
                "startDate": "12/11/2022",
                "endDate": "13/11/2022", 
            }
        }