"""users.create_at

Revision ID: 45a47e5af6f2
Revises: d05bfb568638
Create Date: 2022-12-06 18:37:52.536781

"""
from alembic import op
import sqlalchemy as sa
from app.db.models import users_table

# revision identifiers, used by Alembic.
revision = '45a47e5af6f2'
down_revision = 'd05bfb568638'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('created_at', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###

    op.bulk_insert(users_table,
        [
            {'name':'Пользователь 1'},
            {'name':'Пользователь 2'},
            {'name':'Пользователь 3'},
        ]
    )


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'created_at')
    # ### end Alembic commands ###
