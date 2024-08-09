from fastapi.encoders import jsonable_encoder
from sqlmodel import Session

from app import crud
from app.core.security import verify_password
from app.models import User, UserCreate, UserUpdate
from app.tests.utils.utils import random_email, random_lower_string, random_username
from app.utils import UserRole

def test_create_user(db: Session) -> None:
    email = random_email()
    username = random_username()
    password = random_lower_string()
    user_in = UserCreate(email=email, username=username, password=password)
    user = crud.create_user(session=db, user_create=user_in)
    assert user.email == email
    assert hasattr(user, "hashed_password")


def test_authenticate_user(db: Session) -> None:
    email = random_email()
    username = random_username()
    password = random_lower_string()
    user_in = UserCreate(email=email, username=username, password=password)
    user = crud.create_user(session=db, user_create=user_in)
    authenticated_user = crud.authenticate(session=db, username=username, password=password)
    assert authenticated_user
    assert user.email == authenticated_user.email


def test_not_authenticate_user(db: Session) -> None:
    username = random_username()
    password = random_lower_string()
    user = crud.authenticate(session=db, username=username, password=password)
    assert user is None


def test_check_if_user_is_active(db: Session) -> None:
    email = random_email()
    username = random_username()
    password = random_lower_string()
    user_in = UserCreate(email=email, username=username, password=password)
    user = crud.create_user(session=db, user_create=user_in)
    assert user.is_active is True


def test_check_if_user_is_active_inactive(db: Session) -> None:
    email = random_email()
    username = random_username()
    password = random_lower_string()
    user_in = UserCreate(email=email, username=username, password=password, disabled=True)
    user = crud.create_user(session=db, user_create=user_in)
    assert user.is_active


def test_check_if_user_is_admin(db: Session) -> None:
    email = random_email()
    username = random_username()
    password = random_lower_string()
    user_in = UserCreate(email=email, username=username, password=password, role=UserRole.admin)
    user = crud.create_user(session=db, user_create=user_in)
    assert user.role == UserRole.admin


def test_check_if_user_role_is_normal_user(db: Session) -> None:
    email = random_email()
    username = random_username()
    password = random_lower_string()
    user_in = UserCreate(email=email, username=username, password=password)
    user = crud.create_user(session=db, user_create=user_in)
    assert user.role == UserRole.user


def test_get_user(db: Session) -> None:
    email = random_email()
    username = random_username()
    password = random_lower_string()
    user_in = UserCreate(email=email, username=username, password=password, role=UserRole.admin)
    user = crud.create_user(session=db, user_create=user_in)
    user_2 = db.get(User, user.id)
    assert user_2
    assert user.email == user_2.email
    assert jsonable_encoder(user) == jsonable_encoder(user_2)


def test_update_user(db: Session) -> None:
    email = random_email()
    username = random_username()
    password = random_lower_string()
    user_in = UserCreate(email=email, username=username, password=password, role=UserRole.admin)
    user = crud.create_user(session=db, user_create=user_in)
    new_password = random_lower_string()
    user_in_update = UserUpdate(password=new_password, role=UserRole.admin)
    if user.id is not None:
        crud.update_user(session=db, db_user=user, user_in=user_in_update)
    user_2 = db.get(User, user.id)
    assert user_2
    assert user.email == user_2.email
    assert verify_password(new_password, user_2.hashed_password)
