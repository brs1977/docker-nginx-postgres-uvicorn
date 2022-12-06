from app.schemas.users import UserSchema
from app.db.session import database
from app.db.models import users


async def post(payload: UserSchema):
    query = users.insert().values(name=payload.name)
    return await database.execute(query=query)

async def get(id: int):
    query = users.select().where(id == users.c.id)
    return await database.fetch_one(query=query)


async def get_all():
    query = users.select()
    return await database.fetch_all(query=query)


async def put(id: int, payload: UserSchema):
    query = (
        users
        .update()
        .where(id == users.c.id)
        .values(name=payload.name)
        .returning(users.c.id)
    )
    return await database.execute(query=query)


async def delete(id: int):
    query = users.delete().where(id == users.c.id)
    return await database.execute(query=query)    