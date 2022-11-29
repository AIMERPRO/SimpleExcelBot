"""initial

Revision ID: 067ef0dbd8e1
Revises: 23bb016a42c6
Create Date: 2022-11-29 07:09:35.796186

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '067ef0dbd8e1'
down_revision = '23bb016a42c6'
branch_labels = None
depends_on = None


# Add two default Roles into DataBase on startup

def upgrade() -> None:
    op.execute("INSERT INTO roles (id, name) VALUES (1, 'Грузчик')")
    op.execute("INSERT INTO roles (id, name) VALUES (2, 'Дворник')")


def downgrade() -> None:
    pass
