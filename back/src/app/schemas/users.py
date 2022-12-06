from pydantic import BaseModel


class UserSchema(BaseModel):
    name: str    

class UserDB(UserSchema):
    id: int    