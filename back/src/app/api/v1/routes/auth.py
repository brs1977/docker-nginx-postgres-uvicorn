from fastapi import APIRouter, Depends, Response, Request
from loguru import logger

# from app.api.security import manager, authenticate_user
from app.api import security
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.users import Token, UserLogin

router = APIRouter()


@router.post("/login", status_code=201)
async def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends()) -> dict:
    user = await security.authenticate_user(form_data.username, form_data.password)
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

    # security.set_access_token(user.username, request.client.host, response)
    security.set_access_token(user.username, response)
    return {"status": "Success"}


@router.get("/me", response_model=UserLogin)
async def read_users_me(current_user=Depends(security.manager)) -> UserLogin:
    return current_user


@router.get("/logout", status_code=200)
async def logout(response: Response):
    response.delete_cookie("access-token")
    return {"status": "Success"}
