from fastapi import APIRouter
from app.api.v1.routes import users
from app.api.v1.routes import structure_formations

api_router = APIRouter()

api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(
    structure_formations.router,
    prefix="/structure_formations",
    tags=["structure_formations"],
)
