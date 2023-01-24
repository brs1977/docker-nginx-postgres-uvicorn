from fastapi import APIRouter, Depends, Response
from app.api.security import manager, authenticate_user
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.users import Token, UserLogin

router = APIRouter()

@router.post('/login', status_code=201)
async def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends())-> map:
    user = await authenticate_user(form_data.username, form_data.password)
    token = manager.create_access_token(data={'sub': user.username})
    manager.set_cookie(response, token)
    return {'status': 'Success'}

@router.get("/me", response_model=UserLogin)
async def read_users_me(current_user = Depends(manager)) -> UserLogin:
    return current_user

