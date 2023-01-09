from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class AppModel(BaseModel):
    class Config:
        orm_mode = True


class TokenBase(AppModel):
    """Return response data"""

    access_token: str
    expires: datetime
    token_type: Optional[str] = "bearer"


class Token(AppModel):
    access_token: str
    token_type: str


class TokenData(AppModel):
    username: str | None = None


class UserBase(AppModel):
    """Return response data"""

    id: int
    role_id: int
    email: EmailStr
    username: str
    password: str
    fio: str
    is_active: bool


class UserSchema(AppModel):
    """Validate request data"""

    role_id: int
    email: EmailStr
    username: str
    password: str
    fio: str


class UserDB(UserSchema):
    id: int
