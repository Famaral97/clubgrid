"""add name_has_number to clubs

Revision ID: 856a4fd9cc88
Revises: 761addfa3fc8
Create Date: 2024-10-17 09:56:47.409039

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '856a4fd9cc88'
down_revision: Union[str, None] = '761addfa3fc8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('clubs', sa.Column('name_has_number', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('clubs', 'name_has_number')
    # ### end Alembic commands ###
