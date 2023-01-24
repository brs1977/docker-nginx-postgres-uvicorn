import os
from fastapi import APIRouter, Depends, Response
from fastapi_login import LoginManager
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login.exceptions import InvalidCredentialsException
from app.schemas.users import Token, UserLogin
from datetime import timedelta
from app.db.repository.users import get_by_username

SECRET_KEY = os.environ["SECRET_KEY"]
router = APIRouter()

manager = LoginManager(
    SECRET_KEY, 
    '/login',
    default_expiry=timedelta(minutes=15),
    use_cookie=True,
    use_header=False
)

@manager.user_loader()
async def get_user_by_name(username: str) -> UserLogin:
    user = await get_by_username(username)
    return user


def hash_password(plaintext: str):
    return manager.pwd_context.hash(plaintext)


def verify_password(plaintext: str, hashed: str):
    return manager.pwd_context.verify(plaintext, hashed)


async def authenticate_user(username: str, password: str):
    user = await get_by_username(username)
    if not user:
        raise InvalidCredentialsException
    if not user.is_active:
        raise InvalidCredentialsException
    if not verify_password(password, user.password):
        raise InvalidCredentialsException
    return user


@router.post('/login', status_code=201)
async def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends())-> map:
    user = await authenticate_user(form_data.username, form_data.password)
    token = manager.create_access_token(data={'sub': user.username})
    manager.set_cookie(response, token)
    return {'status': 'Success'}

@router.get("/me", response_model=UserLogin)
async def read_users_me(current_user = Depends(manager)) -> UserLogin:
    return current_user

