from pymongo import MongoClient
import bcrypt

import os
from uuid import uuid4
import datetime

class Database:
    def __init__(self):
        self.client = MongoClient(os.getenv('MONGO_URI'))
        self.core = self.client.core
        self.users = self.core.users

    def get_user(self, username):
        return self.users.find_one({'username': username})

    def get_user_by_id(self, user_id):
        return self.users.find_one({'_id': user_id})

    def get_user_by_email(self, email):
        return self.users.find_one({'email': email})

    def register_user(self, username, email, password):
        password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        data = {
            '_id': str(uuid4()),
            'username': username,
            'email': email,
            'password': password,
            'created_at': datetime.datetime.utcnow(),
            'is_verified': False
        }
        self.users.insert_one(data)
        del data['password']
        return data