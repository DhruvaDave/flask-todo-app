"""Add deafult list

Revision ID: 0001
Revises: 
Create Date: 2021-09-05 18:45:37.138539

"""
from alembic import op
import sqlalchemy as sa
from todo_app.common.constants import MY_LIST


# revision identifiers, used by Alembic.
revision = '0001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.execute(f"INSERT INTO tbl_todo_lists (name) VALUES ('{MY_LIST}')")


def downgrade():
    pass
