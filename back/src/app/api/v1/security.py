from fastapi import Depends, HTTPException, status
from passlib.context import CryptContext
import os
from datetime import datetime, timedelta
import jwt
from jwt import PyJWTError as JWTError
from fastapi.security import OAuth2PasswordBearer
from app.schemas.users import UserDB, TokenData
from app.db.repository.users import get_by_username
from app.config import settings

# from dotenv import load_dotenv
# load_dotenv(dotenv_path='back/.env.dev')


ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days
ALGORITHM = "HS256"
JWT_SECRET_KEY = os.environ["JWT_SECRET_KEY"]  # should be kept secret
JWT_REFRESH_SECRET_KEY = os.environ["JWT_REFRESH_SECRET_KEY"]  # should be kept secret

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.PROJECT_API_VERSION}/users/login", scheme_name="JWT", auto_error=False
)


async def get_page_user(token: str = Depends(oauth2_scheme)):
    if not token:
        return None
    payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
    username = payload.get("sub")
    if username is None:
        return None
    token_data = TokenData(username=username)
    return await get_by_username(username=token_data.username)


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await get_by_username(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: UserDB = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def get_access_token_expires():
    return timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)


def verify_password(plain_password, hashed_password):
    return password_context.verify(plain_password, hashed_password)


async def authenticate_user(username: str, password: str):
    user = await get_by_username(username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
