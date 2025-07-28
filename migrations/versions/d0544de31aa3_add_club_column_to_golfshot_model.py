"""add club column to golfshot model

Revision ID: d0544de31aa3
Revises: dac5953070aa
Create Date: 2025-06-28 16:00:30.253518

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd0544de31aa3'
down_revision: Union[str, None] = 'dac5953070aa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
