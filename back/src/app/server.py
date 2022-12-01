from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import users
from app import model 
from app.db import database

app = FastAPI()

origins = [
    "*"
]

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


@app.get("/")
async def db_test():
    return model.databases()

# @app.get("/users")
# async def db_users():
#     return model.users()  


app.include_router(users.router, prefix="/users", tags=["users"])    
