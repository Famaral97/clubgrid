"""add more information regarding competitions and IG followers

Revision ID: 2e26e6ef8221
Revises: 8a5d63042a14
Create Date: 2024-11-04 18:39:05.290845

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2e26e6ef8221'
down_revision: Union[str, None] = '8a5d63042a14'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('clubs', sa.Column('national_supercup_runner_up', sa.Integer(), nullable=True))
    op.add_column('clubs', sa.Column('cups_winners_cup_runner_up', sa.Integer(), nullable=True))
    op.add_column('clubs', sa.Column('instagram_followers', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('clubs', 'instagram_followers')
    op.drop_column('clubs', 'cups_winners_cup_runner_up')
    op.drop_column('clubs', 'national_supercup_runner_up')
    # ### end Alembic commands ###