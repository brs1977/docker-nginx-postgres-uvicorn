from app.schemas.structure_formations import StructureFormationsSchema
from app.db.session import database
from app.db.models import structure_formations


async def post(payload: StructureFormationsSchema):
    query = structure_formations.insert().values(name=payload.name, pid=payload.pid)
    return await database.execute(query=query)


async def get(id: int):
    query = structure_formations.select().where(id == structure_formations.c.id)
    return await database.fetch_one(query=query)


async def get_all():
    cte = (
        structure_formations.select()
        .where(structure_formations.c.pid == None) # noqa: E711
        .cte("cte", recursive=True)
    )
    union = cte.union_all(
        structure_formations.select().join(cte, structure_formations.c.pid == cte.c.id)
    ).select()

    return await database.fetch_all(query=union)


async def put(id: int, payload: StructureFormationsSchema):
    query = (
        structure_formations.update()
        .where(id == structure_formations.c.id)
        .values(name=payload.name, pid=payload.pid)
        .returning(structure_formations.c.id)
    )
    return await database.execute(query=query)


async def delete(id: int):
    query = structure_formations.delete().where(id == structure_formations.c.id)
    return await database.execute(query=query)
