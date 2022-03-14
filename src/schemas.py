from pydantic import BaseModel, EmailStr, ValidationError, validator
import datetime
from uuid import uuid4
from typing import List, Literal
from enum import Enum

class User(BaseModel):
    name: str
    email: EmailStr
    password: str
    dob: datetime.date
    gender: str
    date_created: datetime.datetime = datetime.datetime.now()
    date_updated: datetime.datetime = datetime.datetime.now()
    @validator('gender')
    def gender_must_be_in_gender(cls, gender):
        genders=["Male", "Female", "Prefer Not To Say"]
        if gender not in genders:
            raise ValueError(f"Must Be A Valid Gender")
        return gender


class EmailSchema(BaseModel):
    email: List[EmailStr]