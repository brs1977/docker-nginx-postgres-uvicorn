from app.db.session import metadata
import sqlalchemy
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    Table,
)

users_table = sqlalchemy.Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String(40), unique=True, index=True, nullable=False),
    Column("username", String(32), unique=True, index=True, nullable=False),
    Column("fio", String(100), nullable=False),
    Column("password", String(256), nullable=False),
    Column(
        "is_active",
        Boolean(),
        server_default=sqlalchemy.sql.expression.true(),
        nullable=False,
    ),
    Column("role_id", Integer, ForeignKey("roles.id")),
)

roles_table = sqlalchemy.Table(
    "roles",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(32), unique=True, nullable=False),
)


structure_formations_table = Table(
    "structure_formations",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("pid", Integer),
    Column("name", String(32)),
)
