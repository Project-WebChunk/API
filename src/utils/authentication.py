from fastapi import exceptions, status
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
import jwt

import os

from src.dependecies import database, User, EmailSchema



conf = ConnectionConfig(
    MAIL_USERNAME = os.environ.get("EMAIL"),
    MAIL_PASSWORD = os.environ.get("PASSWORD"),
    MAIL_FROM = os.environ.get("EMAIL"),
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_TLS = True,
    MAIL_SSL = False,
    USE_CREDENTIALS = True
)


async def send_email(email : list, instance: User):

    token_data = {
        "id" : instance._id,
        "username" : instance.username
    }

    token = jwt.encode(token_data, os.environ.get("TOKEN"))
    template = f"""
        <!DOCTYPE html>
        <html>
        <head>
        </head>
        <body>
        <h1 style="text-align: center;">
        Jangle Email Verification
        </h1>
        <div>
        <br/>
        </div>
        <h3 style="text-align: center;">
        <font size="5">
        Thank You For Choosing Jangle! Please
        <a href="{os.environ.get("DOMAIN")}/auth/verify?token={token}"" target="_blank">
        Click this link
        </a>
        to Verify your account :)
        </font>
        </h3>
        <div>
        <font size="5">
        <br/>
        </font>
        </div>
        <div>
        <font size="5">
        <br/>
        </font>
        </div>
        <div style="text-align: center;">
        <font size="5">
        #OpenSourceForever
        </font>
        </div>
        </body>
        </html>
    """

    message = MessageSchema(
        subject="Jangle Account Verification Mail",
        recipients=email,
        body=template,
        subtype="html"
        )

    fm = FastMail(conf)
    await fm.send_message(message) 
    
async def verify_token(token: str):
    data = jwt.decode(token, os.environ.get("TOKEN"))
    user = database.get_user_by_id(data["id"])
    if user:
        return user
    else:
        raise exceptions.HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )