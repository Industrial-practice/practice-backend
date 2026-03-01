"""fix training session status2v

Revision ID: 19019ff9b619
Revises: 02830bd0b8c1
Create Date: 2026-03-01 01:25:55.784851

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '19019ff9b619'
down_revision: Union[str, Sequence[str], None] = '02830bd0b8c1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
