from fastapi import (FastAPI, Request, Response)
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from uuid import uuid4
import random
import os

try:
    load_dotenv()
except:
    pass

app = FastAPI()

VERSION = "0.0.1-development"

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
    return {"status": "success", "version": VERSION}
