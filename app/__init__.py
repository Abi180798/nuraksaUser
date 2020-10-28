from fastapi import FastAPI, Response
from fastapi.security import OAuth2PasswordBearer
from fastapi.testclient import TestClient
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_main():
    return {"msg": "Hello World"}

from .router import *

client = TestClient(app)