from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from .user import decode_jwt_token
upload_bp = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@upload_bp.get("/upload")
async def video(token: Annotated[str, Depends(oauth2_scheme)]):
    payload = decode_jwt_token(token=token)
    username: str = payload.get("sub")
    return {"logged_in_as": username}