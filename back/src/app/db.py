from databases import Database
from app.config import settings
from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    MetaData,
    String,
    Table,
    create_engine
)
from sqlalchemy.sql import func

# db = create_engine(settings.DATABASE_URL)

metadata = MetaData()
users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(32)),
)

# databases query builder
database = Database(settings.DATABASE_URL)