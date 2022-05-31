from pymongo import MongoClient
import bcrypt
import jwt

import os
from uuid import uuid4
import datetime
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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
        self.send_mail(data['_id'])
        del data['password']
        return data

    def send_mail(self, user_id):
        user = self.get_user_by_id(user_id)
        message = MIMEMultipart("alternative")
        message["Subject"] = "Verify your email"
        message["From"] = os.getenv('EMAIL')
        message["To"] = user['email']

        encoded = jwt.encode({'_id': user['_id']}, os.getenv('TOKEN'), algorithm='HS256')

        url = os.getenv('DOMAIN') + '/auth/verify?token=' + encoded

        html = """
        <h1 style="text-align: center;">Webchunk Email Verification</h1>
        <br>
        <h3 style="text-align: center;">
            <font size="5">
                Hello {user},
                <br>
                Thank You For Choosing Webchunk! Please <a href="{url}" target="_blank">Click this link</a> to Verify your account :)
            </font>
        </h3>
        <br>
        <br>
        <div style="text-align: center;">
            <font size="5">#OpenSourceForever</font>
        </div>
        """.format(user=user['username'], url=url)

        html = MIMEText(html, "html")
        message.attach(html)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(os.getenv('EMAIL'), os.getenv('PASSWORD'))
            server.sendmail(os.getenv('EMAIL'), user['email'], message.as_string())

    def verify_user(self, user_id):
        self.users.update_one({'_id': user_id}, {'$set': {'is_verified': True}})

    def set_user_token(self, user_id):
        user = self.get_user_by_id(user_id)
        if user:
            token = {
                "user_id": user_id,
                "email": user['email'],
                "created_at": datetime.datetime.timestamp(datetime.datetime.utcnow()),
                "expires_at": datetime.datetime.timestamp(datetime.datetime.utcnow() + datetime.timedelta(days=30))
            }
            token = jwt.encode(token, os.getenv('TOKEN'), algorithm='HS256')
            self.users.update_one({'_id': user['_id']}, {'$set': {'token': token}})
            return token

    def check_token(self, token):
        try:
            decoded = jwt.decode(token, os.getenv('TOKEN'), algorithms=['HS256'])
            current_time = datetime.datetime.timestamp(datetime.datetime.utcnow())
            if decoded['expires_at'] < current_time:
                return False
            return True
        except:
            return "Invalid Token"


    def authenticate_user(self, email, password):
        user = self.get_user_by_email(email)
        if not user:
            return "Email not found"
        if not bcrypt.checkpw(password.encode('utf-8'), user['password']):
            return "Password is incorrect"
        # del user['password']
        # return user
        if 'token' not in user:
            token = self.set_user_token(user['_id'])
        else:
            if self.check_token(user['token']):
                token = user['token']
            else:
                token = self.set_user_token(user['_id'])
        return {"token": token}