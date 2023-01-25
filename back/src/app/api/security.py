import os
from fastapi import Response
from fastapi_login import LoginManager
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login.exceptions import InvalidCredentialsException
from app.schemas.users import UserLogin
from datetime import timedelta
from app.db.repository import users

ACCESS_TOKEN_EXPIRE_HOURS = 1
SECRET_KEY = os.environ["SECRET_KEY"]
manager = LoginManager(
    SECRET_KEY, 
    '/login',
    # default_expiry=timedelta(minutes=15),
    default_expiry=timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS),    
    use_cookie=True,
    use_header=False
)

@manager.user_loader()
async def get_user_by_name(username: str) -> UserLogin:
    return await users.get_by_username(username)


def hash_password(plaintext: str):
    return manager.pwd_context.hash(plaintext)


def verify_password(plaintext: str, hashed: str):
    return manager.pwd_context.verify(plaintext, hashed)


async def authenticate_user(username: str, password: str) -> UserLogin:
    user = await users.get_by_username(username)
    if not user:
        raise InvalidCredentialsException
    if not verify_password(password, user.password):
        raise InvalidCredentialsException
    return user

def set_access_token(username: str, response: Response):
    token = manager.create_access_token(data={'sub': username})
    manager.set_cookie(response, token)

    
