"""Change angle_h and lateral to String

Revision ID: 776145fafc40
Revises: 31bdff04a851
Create Date: 2025-08-18 19:55:01.900415

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '776145fafc40'
down_revision: Union[str, None] = '31bdff04a851'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('drive_range_shots_new',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('club', sa.String(25)),
    sa.Column('ball_speed', sa.Float(), nullable=False),
    sa.Column('angle_v', sa.Float(), nullable=False),
    sa.Column('angle_h', sa.String(8), nullable=False),
    sa.Column('carry', sa.Float(), nullable=False),
    sa.Column('roll', sa.Float(), nullable=False),
    sa.Column('total', sa.Float(), nullable=False),
    sa.Column('lateral', sa.String(8), nullable=False),
    sa.Column('spin', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )

    op.drop_table('drive_range_shots')
    op.rename_table('drive_range_shots_new', 'drive_range_shots')


def downgrade() -> None:
    op.create_table('drive_range_shots_old',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('club', sa.String(25)),
    sa.Column('ball_speed', sa.Float(), nullable=False),
    sa.Column('angle_v', sa.Float(), nullable=False),
    sa.Column('angle_h', sa.Float(), nullable=False),
    sa.Column('carry', sa.Float(), nullable=False),
    sa.Column('roll', sa.Float(), nullable=False),
    sa.Column('total', sa.Float(), nullable=False),
    sa.Column('lateral', sa.Float(), nullable=False),
    sa.Column('spin', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )

    op.drop_table('drive_range_shots')
    op.rename_table('drive_range_shots_old', 'drive_range_shots')
