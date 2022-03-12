from pymongo import MongoClient
import pyrebase
from uuid import uuid4
import random
from datetime import datetime
import re
import os
import bcrypt

class Database:
    def __init__(self):
        self.client = MongoClient(os.getenv("MONGO_URI"))
        self.db = self.client['core']
        self.users = self.db['users']
    
    def get_user_by_email(self, email):
        return self.users.find_one({"email": email})
    
    def get_user_by_id(self, user_id):
        return self.users.find_one({"_id": user_id})
    
    def create_user(self, userObj: dict):
        salt = bcrypt.gensalt()
        password = bcrypt.hashpw(userObj['password'].encode('utf-8'), salt)
        userObj['password'] = password
        userObj['salt'] = salt
        userObj['_id'] = str(uuid4())
        userObj['dob'] = userObj['dob'].strftime("%Y-%m-%d")
        self.users.insert_one(userObj)
        return userObj