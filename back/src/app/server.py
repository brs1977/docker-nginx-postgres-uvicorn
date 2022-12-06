from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.route import api_router
from app.db.session import database
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

app.include_router(api_router, prefix='/api/v1')
