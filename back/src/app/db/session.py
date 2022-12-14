from databases import Database
from app.config import settings
from sqlalchemy import MetaData
import logging

logging.basicConfig()
# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
logging.getLogger("sqlalchemy").setLevel(logging.INFO)

# from sqlalchemy import create_engine

# db = create_engine(settings.DATABASE_URL)

metadata = MetaData()

# databases query builder
database = Database(settings.DATABASE_URL)
