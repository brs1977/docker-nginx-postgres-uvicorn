from app.db.session import metadata
import datetime
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
    Column("created_at", DateTime, default=datetime.datetime.utcnow),
)

structure_formations = Table(
    "structure_formations",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("pid", Integer),
    Column("name", String(32)),
)