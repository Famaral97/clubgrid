"""add clubs competitions info

Revision ID: 8a5d63042a14
Revises: 2b9fbd8010ce
Create Date: 2024-10-31 19:18:42.125688

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8a5d63042a14'
down_revision: Union[str, None] = '2b9fbd8010ce'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('clubs', sa.Column('national_supercup_titles', sa.Integer(), nullable=True))
    op.add_column('clubs', sa.Column('cups_winners_cup_titles', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('clubs', 'cups_winners_cup_titles')
    op.drop_column('clubs', 'national_supercup_titles')
    # ### end Alembic commands ###
