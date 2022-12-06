from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from app.api import users
from app import model 
from app.db import database
from app.config import settings

app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/test")
async def db_test():
    return model.databases()

# @app.get("/users")
# async def db_users():
#     return model.users()  



api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])    

app.include_router(api_router, prefix='/api/v1')