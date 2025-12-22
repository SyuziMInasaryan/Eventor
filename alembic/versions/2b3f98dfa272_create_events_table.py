"""create events table

Revision ID: 2b3f98dfa272
Revises: ac8bbe643bdb
Create Date: 2025-11-25 16:34:10.730100

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2b3f98dfa272'
down_revision: Union[str, Sequence[str], None] = '720b6863055e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'events',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(length=255), nullable=False, unique=True),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('image', sa.LargeBinary(), nullable=True),
        sa.Column('category', sa.String(length=255), nullable=True),
        sa.Column('Author', sa.String(length=255), nullable=True),
    )




def downgrade() -> None:
     op.drop_table('events')
