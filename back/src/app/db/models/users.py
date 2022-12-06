from app.db.session import metadata
from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    String,
    Table,
)

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(32)),
)

