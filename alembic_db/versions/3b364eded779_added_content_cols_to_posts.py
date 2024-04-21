"""added content cols to posts

Revision ID: 3b364eded779
Revises: c664f2accf45
Create Date: 2024-04-21 11:48:34.390022

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3b364eded779'
down_revision: Union[str, None] = 'c664f2accf45'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass