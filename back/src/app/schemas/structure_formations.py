from pydantic import BaseModel, Field


class StructureFormationsSchema(BaseModel):
    name: str
    pid: int = Field(None)


class StructureFormationsDB(StructureFormationsSchema):
    id: int
