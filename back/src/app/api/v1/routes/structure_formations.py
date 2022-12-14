from typing import List

from fastapi import APIRouter, HTTPException, Path

from app.db.repository import structure_formations

from app.schemas.structure_formations import (
    StructureFormationsDB,
    StructureFormationsSchema,
)

router = APIRouter()


@router.post("/", response_model=StructureFormationsDB, status_code=201)
async def create_structure_formation(payload: StructureFormationsSchema):
    id = await structure_formations.post(payload)

    response_object = {
        "id": id,
        "pid": payload.pid,
        "name": payload.name,
    }
    return response_object


@router.get("/{id}/", response_model=StructureFormationsDB)
async def read_structure_formation(
    id: int = Path(..., gt=0),
):
    structure_formation = await structure_formations.get(id)
    if not structure_formation:
        raise HTTPException(status_code=404, detail="StructureFormation not found")
    return structure_formation


@router.get("/", response_model=List[StructureFormationsDB])
async def read_all_structure_formations():
    return await structure_formations.get_all()


@router.put("/{id}/", response_model=StructureFormationsDB)
async def update_structure_formation(
    payload: StructureFormationsSchema,
    id: int = Path(..., gt=0),
):
    structure_formation = await structure_formations.get(id)
    if not structure_formation:
        raise HTTPException(status_code=404, detail="StructureFormation not found")

    id = await structure_formations.put(id, payload)

    response_object = {
        "id": id,
        "pid": payload.pid,
        "name": payload.name,
    }
    return response_object


@router.delete("/{id}/", response_model=StructureFormationsDB)
async def delete_structure_formation(id: int = Path(..., gt=0)):
    structure_formation = await structure_formations.get(id)
    if not structure_formation:
        raise HTTPException(status_code=404, detail="StructureFormation not found")

    await structure_formations.delete(id)

    return structure_formation
