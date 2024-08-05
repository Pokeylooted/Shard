import os
from typing import Annotated
import logging
from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer

from .upload import upload_bp
from .user import user_bp

app = FastAPI()

logging.getLogger().setLevel(logging.DEBUG)

# Register blueprints (routers in FastAPI)
app.include_router(upload_bp, prefix="/upload")
app.include_router(user_bp, prefix="/user")

@app.get("/")
async def hello_world():
    return {"message": "Hello World!"}
