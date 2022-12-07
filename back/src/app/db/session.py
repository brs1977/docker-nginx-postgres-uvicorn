from databases import Database
from app.config import settings
from sqlalchemy import MetaData
# from sqlalchemy import create_engine

# db = create_engine(settings.DATABASE_URL)

metadata = MetaData()

# databases query builder
database = Database(settings.DATABASE_URL)
