"""fix training session status

Revision ID: 02830bd0b8c1
Revises: f4c3fe91307d
Create Date: 2026-03-01 01:25:12.654154

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '02830bd0b8c1'
down_revision: Union[str, Sequence[str], None] = 'f4c3fe91307d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
