"""add country property to grids

Revision ID: 9327afffeb27
Revises: 2e607728b518
Create Date: 2025-03-24 09:04:28.291180

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9327afffeb27'
down_revision: Union[str, None] = '2e607728b518'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('grids', sa.Column('country', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('grids', 'country')
    # ### end Alembic commands ###
