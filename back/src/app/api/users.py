from typing import List

from fastapi import APIRouter, HTTPException, Path

from app.api import crud

from app.api.models import UserDB, UserSchema

router = APIRouter()


@router.post("/", response_model=UserDB, status_code=201)
async def create_user(payload: UserSchema):
    id = await crud.post(payload)

    response_object = {
        "id": id,
        "name": payload.name,
    }
    return response_object



@router.get("/{id}/", response_model=UserDB)
async def read_user(id: int = Path(..., gt=0),):
    user = await crud.get(id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/", response_model=List[UserDB])
async def read_all_users():
    return await crud.get_all()


@router.put("/{id}/", response_model=UserDB)
async def update_user(payload: UserSchema, id: int = Path(..., gt=0),):
    user = await crud.get(id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    id = await crud.put(id, payload)

    response_object = {
        "id": id,
        "name": payload.name,
    }
    return response_object


@router.delete("/{id}/", response_model=UserDB)
async def delete_user(id: int = Path(..., gt=0)):
    user = await crud.get(id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await crud.delete(id)

    return user    