"""add tags to the conditions

Revision ID: 2b9fbd8010ce
Revises: c90a9ce31657
Create Date: 2024-10-28 16:37:46.897151

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2b9fbd8010ce'
down_revision: Union[str, None] = 'c90a9ce31657'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('conditions', sa.Column('tags', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('conditions', 'tags')
    # ### end Alembic commands ###