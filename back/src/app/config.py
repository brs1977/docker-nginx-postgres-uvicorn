import os
from typing import Optional

class Settings:
    PROJECT_NAME:str = "Users"
    PROJECT_VERSION:str = "1.0.0"
    PROJECT_API_VERSION:str = '/api/v1'

    DB_NAME:Optional[str] = os.getenv('POSTGRES_DB')
    DB_USER:Optional[str] = os.getenv('POSTGRES_USER')
    DB_PASS:Optional[str] = os.getenv('POSTGRES_PASSWORD')
    DB_HOST:str = 'db'
    DB_PORT:str = '5432'

    DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

settings = Settings()