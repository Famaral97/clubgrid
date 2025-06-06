"""Add deprecation flag to conditions

Revision ID: 2e607728b518
Revises: c6e1ad47070a
Create Date: 2025-02-14 10:29:09.599788

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import expression

# revision identifiers, used by Alembic.
revision: str = '2e607728b518'
down_revision: Union[str, None] = 'c6e1ad47070a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('conditions', sa.Column('deprecated', sa.Boolean(), server_default='0'))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('conditions', 'deprecated')
    # ### end Alembic commands ###
