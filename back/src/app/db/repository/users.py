from app.schemas.users import UserSchema
from app.db.session import database
from app.db.models import users_table


async def post(payload: UserSchema):
    query = users_table.insert().values(name=payload.name)
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
        .values(name=payload.name)
        .returning(users_table.c.id)
    )
    return await database.execute(query=query)


async def delete(id: int):
    query = users_table.delete().where(id == users_table.c.id)
    return await database.execute(query=query)
