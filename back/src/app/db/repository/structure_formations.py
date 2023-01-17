from app.schemas.structure_formations import StructureFormationsSchema
from app.db.session import database
from app.db.models import structure_formations_table


async def post(payload: StructureFormationsSchema):
    query = structure_formations_table.insert().values(name=payload.name, pid=payload.pid)
    return await database.execute(query=query)


async def get(id: int):
    query = structure_formations_table.select().where(id == structure_formations_table.c.id)
    return await database.fetch_one(query=query)


async def get_all():
    cte = (
        structure_formations_table.select()
        .where(structure_formations_table.c.pid == None)  # noqa: E711
        .cte("cte", recursive=True)
    )
    union = cte.union_all(
        structure_formations_table.select().join(cte, structure_formations_table.c.pid == cte.c.id)
    ).select()

    return await database.fetch_all(query=union)


async def put(id: int, payload: StructureFormationsSchema):
    query = (
        structure_formations_table.update()
        .where(id == structure_formations_table.c.id)
        .values(name=payload.name, pid=payload.pid)
        .returning(structure_formations_table.c.id)
    )
    return await database.execute(query=query)


async def delete(id: int):
    query = structure_formations_table.delete().where(id == structure_formations_table.c.id)
    return await database.execute(query=query)
