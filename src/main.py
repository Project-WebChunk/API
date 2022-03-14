from fastapi import (FastAPI, Request, Response)
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import bcrypt

from uuid import uuid4
import random
import os

if os.path.isfile('.env'):
    load_dotenv()

from .schemas import User
from .routes.auth import router as auth_router

__version__ = '0.0.1'

app = FastAPI()
app.include_router(auth_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",
        ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def index():
    return {"status": "success", "version": __version__}
