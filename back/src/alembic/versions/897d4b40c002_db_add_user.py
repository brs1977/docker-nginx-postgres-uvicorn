"""db: add user

Revision ID: 897d4b40c002
Revises: 13adba72734f
Create Date: 2023-01-20 10:28:23.165540

"""
from alembic import op
import sqlalchemy as sa
from app.db.models import roles_table, users_table
from app.api.v1 import security


# revision identifiers, used by Alembic.
revision = '897d4b40c002'
down_revision = '13adba72734f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.bulk_insert(roles_table,
        [
            {'name':'Гость'},
            {'name':'Оператор'},
            {'name':'Функционер'},
            {'name':'Администратор'},
        ]
    )

    op.bulk_insert(users_table,
        [
            {"username": "adm",
            "role_id": 4,
            "password": security.get_hashed_password('adm'),
            "email": "email@email.com",
            "fio": "fio",
            "is_active": True}    
        ]
    )

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    delete(roles_table)
    delete(users_table)
    # ### end Alembic commands ###
