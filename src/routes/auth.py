from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks, UploadFile, File, Form, Request
from fastapi_mail import FastMail, MessageSchema,ConnectionConfig
from fastapi.responses import HTMLResponse
from starlette.requests import Request
from pydantic import BaseModel, EmailStr
from typing import List
import jwt

import os

from src.dependecies import database, userIn, EmailSchema, userDef
from src.utils import authentication

router = APIRouter(
    prefix="/auth",
)



@router.post("/register")
def register(user: userIn):
    if database.get_user_by_email(user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with email {user.email} already exists"
        )
    user = user.dict()
    user = database.create_user(user)
    user = userDef(**user)
    return {"status": "success", "detail": "User registered successfully", "user": user}


@router.post("/verify", response_class=HTMLResponse)
async def verify(request: Request, token: str):
    user = authentication.verify_token(token)
    if user and not user.is_verified:
        return HTMLResponse(
            """
            <!DOCTYPE html>
            <html>
            <head>
            <title>Jangle</title>
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
            Thank You For Choosing Jangle! Your account has been verified successfully.
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
            </body>
            </html>
            """
        )
    