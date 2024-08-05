from datetime import datetime, timedelta, timezone
from typing import Annotated
import os
import jwt
from enum import Enum
from uuid import UUID
from fastapi import FastAPI, APIRouter, Request, HTTPException, Depends, Query, Path, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from pydantic import BaseModel
from .database import insert_user_into_surreal, get_user_from_db, login_user_db
from passlib.context import CryptContext
from passlib.hash import pbkdf2_sha256


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
app = FastAPI()
user_bp = APIRouter()

class User(BaseModel):
    username: str
    password: str
    
class Settings(BaseModel):
    authjwt_secret_key: str = os.getenv('JWT_SECRET_KEY')
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

class UserRole(str, Enum):
    user = "user"
    admin = "admin"

class Token(BaseModel):
    access_token: str
    token_type: str


def verify_password(plain_password, hashed_password):
    return pbkdf2_sha256.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate_user(username: str, password: str):
    hashed_password = get_password_hash(password)
    userid = login_user_db(username=username, passwordhash=hashed_password)
    if not userid:
        return False
    return userid

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, Settings.authjwt_secret_key, algorithm=Settings.algorithm)
    return encoded_jwt

def decode_jwt_token(token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, Settings.authjwt_secret_key, algorithms=[Settings.algorithm])
        return payload
    except InvalidTokenError:
        raise credentials_exception

@user_bp.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=Settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@user_bp.post("/signup", status_code=status.HTTP_201_CREATED)
async def create_user(user: User):
    if not user.username or not user.password:
        raise HTTPException(status_code=400, detail="Username and password are required")
    hash: str = pbkdf2_sha256.hash(user.password)
    user_id = await insert_user_into_surreal(username=user.username, passwordhash=hash, role=UserRole.user)
    return JSONResponse(content={'user_id': user_id}, status_code=201)

@user_bp.get("/user/{user_id}")
async def get_user(user_id: Annotated[UUID, Path(title="The ID of user to retrieve")]):
    user = await get_user_from_db(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@user_bp.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=Settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

app.include_router(user_bp, prefix="/user")