from fastapi import FastAPI
import model

app = FastAPI()


@app.get("/")
async def db_test():
    result = model.databases()  
    return {"тест": str(result)}  

@app.get("/users")
async def db_users():
    return model.users()  
