from databases import Database
from app.config import settings
from sqlalchemy import MetaData

# import logging
# logging.basicConfig()
# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

metadata = MetaData()
database = Database(settings.DATABASE_URL)
