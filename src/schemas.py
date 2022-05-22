from pydantic import BaseModel, EmailStr, ValidationError, validator
import datetime
from uuid import uuid4
from typing import List, Literal
from enum import Enum
from tortoise import Model, fields
from tortoise.contrib.pydantic import pydantic_model_creator

class User(Model):
    _id = fields.CharField(pk=True, max_length=36, default=lambda: str(uuid4()))
    name = fields.CharField(max_length=50)
    email = fields.CharField(max_length=50)
    password = fields.CharField(max_length=35)
    gender = fields.IntField()
    dob = fields.DatetimeField()
    is_verified = fields.BooleanField(default=False)
    joined = fields.DatetimeField(auto_now_add=True)

class EmailSchema(BaseModel):
    email: List[EmailStr]
    
userIn = pydantic_model_creator(User, exclude=['_id', 'salt', 'is_verified', 'joined'], exclude_readonly=True)
userOut = pydantic_model_creator(User, exclude=['password', 'salt'])
userDef = pydantic_model_creator(User)