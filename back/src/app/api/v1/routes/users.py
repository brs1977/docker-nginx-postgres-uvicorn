from typing import List
from fastapi import Path, APIRouter, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.db.repository import users
from app.schemas.users import UserDB, UserSchema, Token
from loguru import logger
from app.api.v1 import security

#     get_current_active_user,
#     get_access_token_expires,
#     authenticate_user,
#     create_access_token,
# )

router = APIRouter()


@router.post("/", response_model=UserDB, status_code=201)
async def create_user(payload: UserSchema):
    payload.password = security.get_hashed_password(payload.password)
    id = await users.post(payload)
    response_object = {
        "id": id,
        "username": payload.username,
        "role_id": payload.role_id,
        "password": payload.password,
        "email": payload.email,
        "fio": payload.fio,
        "is_active": payload.is_active,
    }
    return response_object


@router.get("/{id}/", response_model=UserDB)
async def read_user(
    id: int = Path(..., gt=0),
):
    user = await users.get(id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/", response_model=List[UserDB])
async def read_all_users():
    return await users.get_all()


@router.put("/{id}/", response_model=UserDB)
async def update_user(
    payload: UserSchema,
    id: int = Path(..., gt=0),
):
    user = await users.get(id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    id = await users.put(id, payload)

    response_object = {
        "id": id,
        "username": payload.username,
        "role_id": payload.role_id,
        "password": payload.password,
        "email": payload.email,
        "fio": payload.fio,
        "is_active": payload.is_active,
    }
    return response_object


@router.delete("/{id}/", response_model=UserDB)
async def delete_user(id: int = Path(..., gt=0)):
    user = await users.get(id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await users.delete(id)

    return user


@router.get("/me", response_model=UserDB)
async def read_users_me(
    current_user: UserDB = Depends(security.get_current_active_user),
):
    return current_user


@router.post("/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await security.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = security.get_access_token_expires()
    access_token = security.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    logger.debug({"access_token": access_token, "token_type": "bearer"})
    return {"access_token": access_token, "token_type": "bearer"}
