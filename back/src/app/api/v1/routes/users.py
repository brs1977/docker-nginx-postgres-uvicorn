from typing import List

from fastapi import APIRouter, HTTPException, Path

from app.db.repository import users

from app.schemas.users import UserDB, UserSchema

router = APIRouter()


@router.post("/", response_model=UserDB, status_code=201)
async def create_user(payload: UserSchema):
    id = await users.post(payload)

    response_object = {
        "id": id,
        "name": payload.name,
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
        "name": payload.name,
    }
    return response_object


@router.delete("/{id}/", response_model=UserDB)
async def delete_user(id: int = Path(..., gt=0)):
    user = await users.get(id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await users.delete(id)

    return user
