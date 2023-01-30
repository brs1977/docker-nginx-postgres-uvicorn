import os
from fastapi import Response
from fastapi_login import LoginManager
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login.exceptions import InvalidCredentialsException
from app.schemas.users import UserLogin
from datetime import timedelta
from app.db.repository import users
from fastapi import HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED

# InvalidCredentialsException = HTTPException(
#     status_code=HTTP_401_UNAUTHORIZED,
#     detail="Invalid credentials",
#     headers={"WWW-Authenticate": "Bearer"}
# )


# access-control-allow-credentials: true
# access-control-allow-origin: *
# Connection: keep-alive
# Content-Length: 20
# Content-Type: application/json
# Date: Wed, 25 Jan 2023 07:14:59 GMT
# Server: nginx/1.21.6
# set-cookie: access-token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG0iLCJleHAiOjE2NzQ2MzQ0OTl9.br6oNFRtiosiOEPNg3Xrs7mM_M_1KwZL0mAJc3UNwiQ; HttpOnly; Path=/; SameSite=lax

ACCESS_TOKEN_EXPIRE_HOURS = 1
SECRET_KEY = os.environ["SECRET_KEY"]
manager = LoginManager(
    SECRET_KEY,
    "/login",
    # default_expiry=timedelta(minutes=15),
    default_expiry=timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS),
    use_cookie=True,
    use_header=True,
    custom_exception = InvalidCredentialsException    
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

async def get_current_user(request):
    cookie_name = manager.cookie_name
    token = request.cookies.get(cookie_name)
    try:
        user = await manager.get_current_user(token)
        return user
    except HTTPException as e:
        return None

def set_access_token(username: str, response: Response):
    token = manager.create_access_token(data={"sub": username})
    # response.set_cookie(key="access-token", value=token, secure=True, domain="129.200.0.116")
    manager.set_cookie(response, token)
