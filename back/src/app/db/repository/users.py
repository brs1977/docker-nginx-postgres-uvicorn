from app.schemas.users import UserSchema
from app.db.session import database
from app.db.models import users_table
from typing import Optional


async def get_by_username(username: Optional[str]):
    query = users_table.select().where(username == users_table.c.username)
    return await database.fetch_one(query=query)


async def post(payload: UserSchema):
    query = users_table.insert().values(
        username=payload.username,
        password=payload.password,
        fio=payload.fio,
        email=payload.email,
        role_id=payload.role_id,
        is_active=payload.is_active,
    )
    return await database.execute(query=query)


async def get(id: int):
    query = users_table.select().where(id == users_table.c.id)
    return await database.fetch_one(query=query)


async def get_all():
    query = users_table.select()
    return await database.fetch_all(query=query)


async def put(id: int, payload: UserSchema):
    query = (
        users_table.update()
        .where(id == users_table.c.id)
        .values(
            username=payload.username,
            password=payload.password,
            fio=payload.fio,
            email=payload.email,
            role_id=payload.role_id,
            is_active=payload.is_active,
        )
        .returning(users_table.c.id)
    )
    return await database.execute(query=query)


async def delete(id: int):
    query = users_table.delete().where(id == users_table.c.id)
    return await database.execute(query=query)
