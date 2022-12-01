from fastapi import FastAPI
from app import model 

app = FastAPI()


@app.get("/")
async def db_test():
    return model.databases()

@app.get("/users")
async def db_users():
    return model.users()  
