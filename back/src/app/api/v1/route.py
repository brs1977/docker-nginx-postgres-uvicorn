from fastapi import APIRouter
from app.api.v1.routes import auth, users, config, menu, page, structure_formations

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(menu.router, prefix="/menu", tags=["menu"])
api_router.include_router(page.router, prefix="/page", tags=["page"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(config.router, prefix="/config", tags=["config"])
api_router.include_router(
    structure_formations.router,
    prefix="/structure_formations",
    tags=["structure_formations"],
)
